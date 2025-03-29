from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service as ChromiumService
from datetime import datetime, timedelta
import os

def renew(username, password):
    chrome_options = Options()
    options = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--remote-debugging-port=9222",
        "--headless=new",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(
        service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), 
        options=chrome_options
    )

    driver.get('https://licenseportal.it.chula.ac.th/')
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.ID, 'UserName')))
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'Password')
    password_input.send_keys(password)

    signin_button = driver.find_element(By.XPATH, '//button')
    signin_button.click()

    driver.get('https://licenseportal.it.chula.ac.th/Home/Borrow')

    expiry_date_input = wait.until(EC.presence_of_element_located((By.ID, 'ExpiryDateStr')))
    week = datetime.now() + timedelta(days=7)
    driver.execute_script("arguments[0].value = arguments[1];", expiry_date_input, week.strftime('%d/%m/%Y'))

    select_element = driver.find_element(By.ID, 'ProgramLicenseID')
    Select(select_element).select_by_value('5')

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loading')))

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    driver.execute_script("arguments[0].click();", save_button)

    driver.quit()

    return True

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
renew(USERNAME, PASSWORD)
