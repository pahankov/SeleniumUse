from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import allure

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

# Тест 1
@allure.title("Тест на авторизацию с неверными данными")
@allure.description("Проверка, что система корректно показывает ошибку при вводе неправильного логина/пароля.")
@allure.feature("Авторизация")

def test_unsuccessful_login(driver):

    with allure.step("Открыть страницу входа"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести некорректный логин 'Ivanov'"):
        text_input_login = driver.find_element("id", "username")
        text_input_login.send_keys("Ivanov")

    with allure.step("Ввести некорректный пароль '123RUS'"):
        text_input_password = driver.find_element("id", "password")
        text_input_password.send_keys("123RUS")

    with allure.step("Нажать кнопку 'Login'"):
        press_button_send = driver.find_element("class name", "radius")
        press_button_send.click()

    with allure.step("Проверить сообщение об ошибке"):
        success_message = driver.find_element("id", "flash")
        assert "Your username is invalid!" in success_message.text
        allure.attach(driver.get_screenshot_as_png(),
            name="sms_error",
            attachment_type=allure.attachment_type.PNG)
# Тест 2
@allure.title("Тест на авторизацию с валидными данными")
@allure.description("Проверка, что система корректно осуществляет вход при вводе правильного логина/пароля.")
@allure.feature("Авторизация")

def test_successful_login(driver):

    with allure.step("Открыть страницу входа"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести логин 'tomsmith'"):
        text_input_login = driver.find_element("id", "username")
        text_input_login.send_keys("tomsmith")

    with allure.step("Ввести пароль 'SuperSecretPassword!'"):
        text_input_password = driver.find_element("id", "password")
        text_input_password.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку 'Login'"):
        press_button_send = driver.find_element("class name", "radius")
        press_button_send.click()

    with allure.step("Проверить сообщение об успешном входе"):
        success_message = driver.find_element("id", "flash")
        assert "You logged into a secure area!" in success_message.text
        allure.attach(driver.get_screenshot_as_png(),
            name="sms_incoming",
            attachment_type=allure.attachment_type.PNG)