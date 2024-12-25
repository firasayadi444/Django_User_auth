""""""
import logging
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:4200")
    logging.info("Navigated to http://localhost:4200")

    assert "PixGen" in driver.title, "Page title does not match expected value."
    logging.info("Test Passed: PixGen is accessible.")
except Exception as e:
    logging.error(f"Test Failed: {e}")
finally:
    driver.quit()

