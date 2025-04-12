from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Configuration
LOGIN_URL = "YOUR WEBSITE LOGIN URL"
DASHBOARD_URL = ""YOUR WEBSITE DASHBOARD URL""
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"  # Replace with your correct password
CHROMEDRIVER_PATH = "PASTE YOUR CHROMEDRIVERPATH HERE "

def create_driver():
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Create the Chrome driver instance with the Service object
    service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def login(driver):
    print("[*] Logging in...")
    driver.get(LOGIN_URL)
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    # Check if login was successful (if redirected to the dashboard)
    return driver.current_url == DASHBOARD_URL

def keep_session_alive(driver):
    while True:
        driver.get(DASHBOARD_URL)
        time.sleep(2)

        # If logged out, re-login
        if LOGIN_URL in driver.current_url:
            print("[!] Session expired, re-logging in...")
            if not login(driver):
                print("[x] Re-login failed.")
                break
            print("[+] Re-login successful.")
        else:
            print("[✓] Session still alive.")

        # Check every 5 minutes
        time.sleep(300)

def main():
    driver = create_driver()
    
    # Attempt to log in initially
    if login(driver):
        print("[+] Login successful. Monitoring session...")
        keep_session_alive(driver)
    else:
        print("[x] Initial login failed.")

if __name__ == "__main__":
    main()
