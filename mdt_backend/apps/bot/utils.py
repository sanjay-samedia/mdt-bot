import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager



# Sample North America proxy list (replace with real proxies from a provider)
NA_PROXIES = [
    "http://123.45.67.89:8080",  # Example proxy (US)
    "http://98.76.54.32:3128",   # Example proxy (Canada)
]


def get_headless_browser():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Add proxy
    proxy = random.choice(NA_PROXIES)
    options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def simulate_traffic(driver, url, requested_visits, min_stay_time, max_stay_time):
    print("driver:", driver)
    print("url:", url)
    time.sleep(60)
    # driver.get(url)
    # session_duration = random.uniform(3, 7)  # Random stay time between 3-7 seconds
    # start_time = time.time()

    # # Simulate scrolling
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")  # Scroll halfway
    # time.sleep(random.uniform(0.5, 1.5))
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to bottom
    
    # # Simulate mouse movement
    # actions = ActionChains(driver)
    # actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).perform()
    # time.sleep(random.uniform(0.5, 1))

    # # Simulate random click
    # try:
    #     elements = driver.find_elements("xpath", "//a[@href]")  # Find all links
    #     if elements:
    #         random.choice(elements).click()
    #         time.sleep(random.uniform(1, 2))
    # except Exception as e:
    #     print(f"Click simulation failed: {e}")

    # # Ensure minimum session duration
    # elapsed = time.time() - start_time
    # if elapsed < session_duration:
    #     time.sleep(session_duration - elapsed)

    # return {"url": url, "status": "success", "duration": session_duration}