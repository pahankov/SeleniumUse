from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def driver():
# Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_unsuccessful_login(driver):

    driver.get("https://the-internet.herokuapp.com/login")

    text_input_login = driver.find_element("id", "username")
    text_input_login.send_keys("Ivanov")

    text_input_password = driver.find_element("id", "password")
    text_input_password.send_keys("123RUS")

    press_button_send = driver.find_element("class name", "radius")
    press_button_send.click()

    success_message = driver.find_element("id", "flash")
    assert "Your username is invalid!" in success_message.text

def test_successful_login(driver):

    driver.get("https://the-internet.herokuapp.com/login")

    text_input_login = driver.find_element("id", "username")
    text_input_login.send_keys("tomsmith")

    text_input_password = driver.find_element("id", "password")
    text_input_password.send_keys("SuperSecretPassword!")

    press_button_send = driver.find_element("class name", "radius")
    press_button_send.click()

    success_message = driver.find_element("id", "flash")
    assert "You logged into a secure area!" in success_message.text
