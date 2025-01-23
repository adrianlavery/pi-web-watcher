import os
import time
import subprocess
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException

# Load environment variables from config.env
load_dotenv('./config.env')

# Set up variables from environment variables
url = os.getenv('URL')
queryText = os.getenv('QUERY_TEXT')
queryTextXPath = os.getenv('QUERY_TEXT_XPATH')
loginUser = os.getenv('LOGIN_USER')
loginPass = os.getenv('LOGIN_PASS')
logFile = time.strftime("%Y%m%d") + os.getenv('LOG_FILE')

# Ensure the logs directory exists
log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging
logging.basicConfig(filename=os.path.join(log_dir, logFile), level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message):
    logging.info(message)

service = Service(executable_path='/usr/bin/chromedriver')
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(service=service, options=chrome_options)

log_message("Starting...")

# Open website
log_message("Opening " + url)
driver.get(url)
driver.implicitly_wait(0.5)

# Login to website
log_message("Logging in")
try:
    email_input = driver.find_element(by=By.ID, value='emailInput')
    password_input = driver.find_element(by=By.ID, value='passwordInput')
    sign_in_button = driver.find_element(by=By.CSS_SELECTOR, value=".btn-primary")
    email_input.send_keys(loginUser)
    password_input.send_keys(loginPass)
    sign_in_button.click()
except NoSuchElementException as e:
    log_message(f"Error during login: {e}")
    driver.quit()
    exit(1)

# wait until login is complete
errors = [NoSuchElementException, ElementNotInteractableException]
try:
    wait = WebDriverWait(driver, timeout=60, poll_frequency=1, ignored_exceptions=errors)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar-brand')))
    assert url in driver.current_url
    log_message("Login successful")
except TimeoutException as e:
    log_message(f"Error waiting for login to complete: {e}")
    driver.quit()
    exit(1)

# Adding a 30s sleep here to give the site time to respond
time.sleep(30)
log_message("Checking for '" + queryText + "' every 30 seconds...")


# Loop to check for queryText every 30 seconds
while True:
    try:
        query_text = driver.find_element(by=By.XPATH, value=queryTextXPath).text
    except NoSuchElementException as e:
        log_message(f"Error finding query text element: {e}")
        driver.quit()
        exit(1)

    if queryText not in query_text:
        log_message("'" + queryText + "' not detected!")
        # Check if the TV is turned on and rpi is active using cec-client
        tv_status = subprocess.run(['echo pow 0.0.0.0 | cec-client -s -d 1 | grep "power status:"'], capture_output=True, text=True, shell=True)
        rpi_status = subprocess.run(['echo scan | cec-client -s -d 1 | grep "currently active source"'], capture_output=True, text=True, shell=True)

        if tv_status.returncode != 0:
            log_message(f"TV status command failed with exit code {tv_status.returncode}")
        if rpi_status.returncode != 0:
            log_message(f"RPI status command failed with exit code {rpi_status.returncode}")
        
        if 'power status: on' in tv_status.stdout and 'currently active source: unknown (-1)' in rpi_status.stdout:
            log_message("TV and pi are on")
        else:
            log_message("TV and pi are off")
            # Make the rpi active on the CEC bus
            activate_rpi = subprocess.run(['echo as 1.0.0.0 | cec-client -s -d 1'], capture_output=True, text=True, shell=True)
            log_message("Activate RPI output: " + activate_rpi.stdout)
            if activate_rpi.returncode != 0:
                log_message(f"Activate RPI command failed with exit code {activate_rpi.returncode}")
            # Signal the TV to turn on
            turn_on_tv = subprocess.run(['echo on 0.0.0.0 | cec-client -s -d 1'], capture_output=True, text=True, shell=True)
            log_message("Turn on TV output: " + turn_on_tv.stdout)
            if turn_on_tv.returncode != 0:
                log_message(f"Turn on TV command failed with exit code {turn_on_tv.returncode}")
            log_message("TV and pi have been activated")
        
        
        # Wait for 30 minutes before continuing the loop
        time.sleep(1800)
        log_message("30 minutes have passed, returning to the loop")
    
    time.sleep(30)

log_message("Exiting...")
driver.quit()