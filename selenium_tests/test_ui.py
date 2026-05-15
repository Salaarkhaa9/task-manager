import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("APP_URL", "http://web-app:5000")

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_page_title_and_header(driver):
    driver.get(APP_URL)
    assert "Simple Web App" in driver.title
    header = driver.find_element(By.ID, "header")
    assert header.text == "Item List"

def test_add_item_ui(driver):
    driver.get(APP_URL)
    input_field = driver.find_element(By.ID, "item-name")
    input_field.send_keys("Selenium Test Item")
    
    add_button = driver.find_element(By.ID, "add-btn")
    add_button.click()
    
    time.sleep(2)
    
    item_list = driver.find_element(By.ID, "item-list")
    assert "Selenium Test Item" in item_list.text
