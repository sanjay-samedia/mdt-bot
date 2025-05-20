import asyncio
import random
from datetime import timedelta
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from aiohttp import ClientSession
from pyppeteer import launch
from pyppeteer.errors import PyppeteerError
from fake_useragent import UserAgent
from celery import shared_task
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import logging
from asgiref.sync import async_to_sync, sync_to_async

from apps.bot.models import BotInstance, BotStatus

logger = logging.getLogger(__name__)

# Proxy list (North America residential proxies - placeholder)
PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
]

class TrafficBot:
    def __init__(self, bot_instance_id: int, website: str, requested_visits: int):
        self.bot_instance_id = bot_instance_id
        self.bot_instance = BotInstance.objects.get(id=bot_instance_id)
        self.website = website
        self.requested_visits = requested_visits
        self.visits_sent = 0
        self.min_stay_time = 1
        self.max_stay_time = 3
        self.start_time = timezone.now()
        self.status = BotStatus.RUNNING
        self.ua = UserAgent()
        self.validate_url()

    def validate_url(self):
        validator = URLValidator()
        try:
            validator(self.website)
        except ValidationError as e:
            logger.error(f"Invalid URL {self.website}: {str(e)}")
            self.status = BotStatus.FAILED
            raise ValidationError(f"Invalid URL: {self.website}")

    async def send_single_aiohttp_visit(self, session: ClientSession) -> bool:
        """Send a single aiohttp visit."""
        try:
            proxy = random.choice(PROXIES)
            headers = {"User-Agent": self.ua.random}
            async with session.get(self.website, headers=headers, timeout=10) as response:
                if response.status == 200:
                    await asyncio.sleep(random.uniform(self.min_stay_time, self.max_stay_time))
                    return True
                else:
                    logger.warning(f"Failed visit to {self.website}: Status {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error in aiohttp visit to {self.website}: {str(e)}")
            return False

    async def send_aiohttp_traffic(self, session: ClientSession, num_visits: int) -> int:
        """Send traffic using aiohttp with high concurrency."""
        successful_visits = 0
        batch_size = 50  # Process 50 concurrent requests
        for i in range(0, num_visits, batch_size):
            batch_visits = min(batch_size, num_visits - i)
            tasks = [self.send_single_aiohttp_visit(session) for _ in range(batch_visits)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            successful_visits += sum(1 for r in results if r is True)
            self.visits_sent += batch_visits
            logger.info(f"*{self.visits_sent} - aiohttp*")
            if self.visits_sent % 1000 == 0:
                await sync_to_async(self.update_bot_instance)()
        return successful_visits

    async def send_pyppeteer_traffic(self, num_visits: int) -> int:
        """Process Pyppeteer visits in a single Celery worker with retries."""
        successful_visits = 0
        browser = None
        page = None
        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Launch browser with Docker-friendly options
                browser = await launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-gpu',
                        '--window-size=1280,720',
                        '--disable-dev-shm-usage',
                        '--shm-size=2g',
                        f'--user-agent={self.ua.random}',
                    ],
                    handleSIGINT=False,
                    handleSIGTERM=False,
                    handleSIGHUP=False,
                )
                logger.info("Pyppeteer browser launched successfully")
                page = await browser.newPage()
                await page.setViewport({'width': 1280, 'height': 720})

                for _ in range(num_visits):
                    for page_attempt in range(max_retries):
                        try:
                            # Navigate with timeout and wait for network idle
                            await page.goto(self.website, {'waitUntil': 'networkidle2', 'timeout': 30000})
                            # Scroll to the bottom
                            await page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
                            # Simulate stay time
                            await asyncio.sleep(random.uniform(self.min_stay_time, self.max_stay_time))
                            successful_visits += 1
                            break  # Exit retry loop on success
                        except PyppeteerError as e:
                            logger.warning(f"Retry {page_attempt + 1}/{max_retries} for page navigation: {str(e)}")
                            if page_attempt == max_retries - 1:
                                logger.error(f"Failed to visit {self.website} after {max_retries} attempts")
                        except Exception as e:
                            logger.error(f"Unexpected error in Pyppeteer visit: {str(e)}")
                            break
                        finally:
                            self.visits_sent += 1
                            logger.info(f"*{self.visits_sent} - browser*")
                            if self.visits_sent % 1000 == 0:
                                await sync_to_async(self.update_bot_instance)()
                break  # Exit browser retry loop on success
            except PyppeteerError as e:
                logger.error(f"Pyppeteer setup attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached for browser launch")
                    self.status = BotStatus.FAILED
            except Exception as e:
                logger.error(f"Unexpected error in Pyppeteer setup: {str(e)}")
                self.status = BotStatus.FAILED
                break
            finally:
                if page:
                    await page.close()
                if browser:
                    await browser.close()
                    logger.info("Pyppeteer browser closed")
        return successful_visits

    def update_bot_instance(self):
        try:
            with transaction.atomic():
                update_data = {
                    'visits_sent': F('visits_sent') + self.visits_sent,
                    'status': self.status,
                }
                if self.status in [BotStatus.COMPLETED, BotStatus.FAILED, BotStatus.RUNNING, BotStatus.STOPPED]:
                    update_data['end_time'] = timezone.now()

                if self.visits_sent <= self.requested_visits:
                    BotInstance.objects.filter(id=self.bot_instance_id).update(**update_data)
                logger.debug(f"Updated BotInstance {self.bot_instance_id} at {self.visits_sent} visits")
        except Exception as e:
            logger.error(f"Failed to update BotInstance {self.bot_instance_id}: {str(e)}")

    def update_status(self, successful_visits: int):
        self.bot_instance.refresh_from_db()
        if not (
            self.bot_instance.status == BotStatus.STOPPED
            and self.bot_instance.updated_at >= timezone.now() - timedelta(hours=24)
        ):
            self.status = (
                BotStatus.COMPLETED if self.visits_sent >= self.requested_visits else BotStatus.RUNNING
            )
            self.update_bot_instance()

@shared_task
def process_traffic_task(bot_instance_id: int, website: str, requested_visits: int, use_pyppeteer: bool = False):
    bot = TrafficBot(bot_instance_id, website, requested_visits)
    bot_instance = BotInstance.objects.get(id=bot_instance_id)
    if (
        bot_instance.status == BotStatus.STOPPED
        and bot_instance.updated_at >= timezone.now() - timedelta(hours=24)
    ):
        logger.info(f"Skipping traffic for BotInstance {bot_instance_id} because it's stopped recently.")
        return {
            "bot_instance_id": bot_instance_id,
            "status": BotStatus.STOPPED,
            "message": "Bot instance was stopped recently (within 24 hours)."
        }
    try:
        if use_pyppeteer:
            async def run_pyppeteer():
                return await bot.send_pyppeteer_traffic(requested_visits)
            successful_visits = async_to_sync(run_pyppeteer)()
        else:
            async def run_aiohttp():
                async with ClientSession() as session:
                    return await bot.send_aiohttp_traffic(session, requested_visits)
            successful_visits = async_to_sync(run_aiohttp)()

        bot.update_status(successful_visits)
        log_data = {
            "bot_instance_id": bot_instance_id,
            "website": bot.website,
            "requested_visits": bot.requested_visits,
            "visits_sent": bot.visits_sent,
            "start_time": bot.start_time,
            "end_time": timezone.now(),
            "min_stay_time": bot.min_stay_time,
            "max_stay_time": bot.max_stay_time,
            "status": bot.status,
        }
        logger.info(f"Bot visits_sent log: {bot_instance.visits_sent}")
        logger.info(f"Bot instance log: {log_data}")
        return log_data
    except Exception as e:
        logger.error(f"Task failed for bot {bot_instance_id}: {str(e)}")
        bot.status = BotStatus.FAILED
        bot.update_bot_instance()
        return {"bot_instance_id": bot_instance_id, "status": BotStatus.FAILED, "error": str(e)}