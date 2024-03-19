import time
import traceback
from multiprocessing import Process, Manager
from bson import ObjectId
import requests
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import capsolver
from db import db
from selenium_logic import create_driver


def get_2fa_code(secret):
    print("Getting 2FA code for secret:", secret)
    response = requests.get(f"https://2fa.live/tok/{secret}")
    token = response.json()['token']
    return token


def auth_process(shared_dict, account_id):
    driver = None
    try:
        account = db['accounts'].find_one({'_id': ObjectId(account_id)})
        account_config = db['accountconfigs'].find_one({'_id': ObjectId(account["accountConfig"])})
        proxy_url = None
        if 'proxy' in account and account['proxy'] is not None:
            proxy = db['proxies'].find_one({'_id': ObjectId(account["proxy"])})
            print("proxy:", proxy)
            proxy_url = f"http://{proxy['login']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
        if account_config and 'userAgent' in account_config:
            agent = account_config['userAgent']
        else:
            agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.71 Safari/537.36"

        login = account['loginOrPhone']
        password = account['password']

        driver = create_driver(proxy_url, agent)
        driver.get("https://twitter.com/i/flow/login")
        # # driver.wait(until.elementLocated(By.css('selector-for-funcaptcha')), 10000);
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'selector-for-funcaptcha')))
        # # driver.findElement(By.css('selector-for-funcaptcha')).click();
        # driver.find_element(By.CSS_SELECTOR, 'selector-for-funcaptcha').click()
        print("Opened Twitter")
        time.sleep(30)
        input_login = driver.find_element(By.XPATH, '//input[@type="text"]')
        for char in login:
            input_login.send_keys(char)
            time.sleep(0.1)
        time.sleep(1)
        input_login.send_keys(Keys.ENTER)
        time.sleep(3)
        print("Entered login successfully")
        input_password = driver.find_element(By.XPATH, '//input[@name="password"]')
        for char in password:
            input_password.send_keys(char)
            time.sleep(0.1)
        time.sleep(1)
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)
        print("Entered password successfully")
        code = get_2fa_code(account['twoFactorAuthCode'])

        input_code = driver.find_element(By.XPATH, '//input[@type="text"]')
        for char in code:
            input_code.send_keys(char)
            time.sleep(0.1)
        time.sleep(1)
        input_code.send_keys(Keys.ENTER)
        time.sleep(5)

        if "Your account has been locked." in driver.page_source:
            print("Account locked")
            driver.find_element(By.XPATH, '//input[@type="submit"]')\
                .click()
            time.sleep(300)
            print("Clicked Start")

            driver.find_element(By.XPATH, '//input[@type="submit"]')\
                .click()

        time.sleep(300)
        print("Entered 2FA code successfully")
        cookies = driver.get_cookies()
        account_config['fullCookies'] = cookies

        parsed_cookies = {}
        for cookie in cookies:
            parsed_cookies[cookie['name']] = cookie['value']

        account_config['cookies'] = parsed_cookies
        db['accountconfigs'].update_one({'_id': account_config['_id']}, {"$set": account_config})
        result = "Authenticated"  # This should be the result of the auth logic
        shared_dict['result'] = "Authenticated"
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        shared_dict['result'] = f"WebDriver error: {e}"
    except Exception as e:
        print("Error authenticating:", str(e))
        shared_dict['result'] = f"Error authenticating auth_process: {str(e)}\n{traceback.format_exc()}"
    finally:
        if driver:
            try:
                driver.close()
            except Exception as e:  # Catching a broader exception if WebDriverException is not enough
                print(f"Failed to close WebDriver properly: {e}")


def auth(account_id):
    try:
        with Manager() as manager:
            shared_dict = manager.dict()
            process = Process(target=auth_process, args=(shared_dict, account_id))
            process.start()
            process.join()  # Wait for the process to finish

            result = shared_dict.get('result', "Process did not return a result")
            return result
    except Exception as e:
        print("Error in auth function:", str(e))
        raise e
