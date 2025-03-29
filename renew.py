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
        "--headless=new",  # New headless mode for better compatibility
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions"
    ]
    for option in options:
        chrome_options.add_argument(option)

    try:
        # Initialize WebDriver
        print("Starting WebDriver...")
        driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), 
            options=chrome_options
        )

        # Open Login Page
        print("Navigating to license portal login page...")
        driver.get('https://licenseportal.it.chula.ac.th/')

        wait = WebDriverWait(driver, 10)

        # Enter Username
        username_input = wait.until(EC.presence_of_element_located((By.ID, 'UserName')))
        username_input.send_keys(username)
        print("Entered username.")

        # Enter Password
        password_input = driver.find_element(By.ID, 'Password')
        password_input.send_keys(password)
        print("Entered password.")

        # Click Sign-in Button
        signin_button = driver.find_element(By.XPATH, '//button')
        signin_button.click()
        print("Clicked login button.")

        # Navigate to Borrow Page
        driver.get('https://licenseportal.it.chula.ac.th/Home/Borrow')
        print("Navigated to Borrow page.")

        # Wait for Expiry Date Field
        expiry_date_input = wait.until(EC.presence_of_element_located((By.ID, 'ExpiryDateStr')))
        
        # Set Expiry Date to 7 Days from Now
        week = datetime.now() + timedelta(days=7)
        driver.execute_script("arguments[0].value = arguments[1];", expiry_date_input, week.strftime('%d/%m/%Y'))
        print(f"Set expiry date to {week.strftime('%d/%m/%Y')}.")

        # Select Program License
        select_element = driver.find_element(By.ID, 'ProgramLicenseID')
        select = Select(select_element)
        select.select_by_value('5')  # Ensure this value is correct
        print("Selected license.")

        # Click Save Button
        save_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        save_button.click()
        print("Clicked submit button.")

        print("Renewal process completed successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()
        print("Closed WebDriver.")

    return True

# Fetch credentials from environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

if not USERNAME or not PASSWORD:
    print("Error: USERNAME or PASSWORD environment variable is not set.")
else:
    renew(USERNAME, PASSWORD)
