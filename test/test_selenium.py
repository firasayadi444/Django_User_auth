from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service('/usr/bin/chromedriver')  # Path to ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Test: Open PixGen and check title
try:
    driver.get("http://localhost:4200")
    assert "PixGen" in driver.title
    print("Test Passed: PixGen is accessible.")
except Exception as e:
    print(f"Test Failed: {e}")
finally:
    driver.quit()
