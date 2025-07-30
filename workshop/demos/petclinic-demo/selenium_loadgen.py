import random
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def run_selenium_task(owner_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"http://localhost/#!/owners/details/{owner_id}"
        print(f"Visiting: {url}")
        driver.get(url)

        # check the element's text is not empty
        value = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(
                By.CSS_SELECTOR,
                "body > div > div > div > ui-view > owner-details > table:nth-child(2) > tbody > tr:nth-child(1) > td > b"
            ).text.strip()
        )
        print(f"Owner ID {owner_id}: Extracted value: {value}")
    except Exception as e:
        print(f"Error for Owner ID {owner_id}: {e}")
    finally:
        driver.quit()


def main():
    while True:
        owner_ids = random.choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # All possible owner IDs
            weights=[1, 1, 1, 1, 1, 1, 1, 1, 8, 7],      # Bias weights for each ID
            k=10                                          # Generate 10 IDs
        )

        with ThreadPoolExecutor(max_workers=5) as executor:  # 5 threads active at a time
            for owner_id in owner_ids:
                delay = random.uniform(0.25, 0.75) / 4  # Delay in milliseconds (e.g., 62.5 ms - 187.5 ms)
                print(f"Scheduling task for Owner ID {owner_id} with a delay of {delay * 1000:.2f} milliseconds...")
                time.sleep(delay)  # Millisecond delay before submitting the task
                executor.submit(run_selenium_task, owner_id)


if __name__ == "__main__":
    main()
