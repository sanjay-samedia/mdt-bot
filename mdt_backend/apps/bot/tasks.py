# import aiohttp
# from datetime import datetime
# import logging
# from celery import shared_task
# from apps.bot.models import BotInstance
# from asgiref.sync import async_to_sync
# from traffic_bot.traffic_bot_core import TrafficBot


# logger = logging.getLogger(__name__)


# @shared_task
# def process_traffic_task(bot_instance_id: int, website: str, requested_visits: int, use_selenium: bool = False):
#     bot = TrafficBot(bot_instance_id, website, requested_visits)
#     bot_instance = BotInstance.objects.get(id=bot_instance_id)
#     try:
#         if use_selenium:
#             successful_visits = bot.send_selenium_traffic(requested_visits)
#         else:
#             async def run_aiohttp():
#                 async with aiohttp.ClientSession() as session:
#                     return await bot.send_aiohttp_traffic(session, requested_visits)
#             successful_visits = async_to_sync(run_aiohttp)()
                
#         bot.update_status(successful_visits)
#         log_data = {
#             "bot_instance_id": bot_instance_id,
#             "website": bot.website,
#             "requested_visits": bot.requested_visits,
#             "visits_sent": bot.visits_sent,
#             "start_time": bot.start_time,
#             "end_time": datetime.now(),
#             "min_stay_time": bot.min_stay_time,
#             "max_stay_time": bot.max_stay_time,
#             "status": bot.status,
#             "success_rate": bot.success_rate,
#         }
#         logger.info(f"Bot instance log: {log_data}")
#         return log_data
#     except Exception as e:
#         logger.error(f"Task failed for bot {bot_instance_id}: {str(e)}")
#         bot.status = "FAILED"
#         return {"bot_instance_id": bot_instance_id, "status": "FAILED", "error": str(e)}