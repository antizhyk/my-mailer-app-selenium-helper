import time
import traceback
from multiprocessing import Process, Queue
from bson import ObjectId
import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from db import db
from selenium_logic import create_driver


def get_2fa_code(secret):
    print("Getting 2FA code for secret:", secret)
    response = requests.get(f"https://2fa.live/tok/{secret}")
    token = response.json()['token']
    return token


def auth_process(queue, account_id):
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
        print("Opened Twitter")
        time.sleep(30)
        input_login = driver.find_element(By.XPATH, '//input[@type="text"]')
        input_login.send_keys(login)
        time.sleep(1)
        input_login.send_keys(Keys.ENTER)
        time.sleep(3)
        print("Entered login successfully")
        input_password = driver.find_element(By.XPATH, '//input[@name="password"]')
        input_password.send_keys(password)
        time.sleep(1)
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)
        print("Entered password successfully")
        code = get_2fa_code(account['twoFactorAuthCode'])

        input_code = driver.find_element(By.XPATH, '//input[@type="text"]')
        input_code.send_keys(code)
        time.sleep(1)
        input_code.send_keys(Keys.ENTER)
        time.sleep(3)
        print("Entered 2FA code successfully")
        cookies = driver.get_cookies()
        account_config['fullCookies'] = cookies

        parsed_cookies = {}
        for cookie in cookies:
            parsed_cookies[cookie['name']] = cookie['value']

        account_config['cookies'] = parsed_cookies
        db['accountconfigs'].update_one({'_id': account_config['_id']}, {"$set": account_config})
        result = "Authenticated"  # This should be the result of the auth logic
        queue.put(result)
    except Exception as e:
        print("Error authenticating:", str(e))
        queue.put(f"Error authenticating auth_process: {str(e)}\n{traceback.format_exc()}")
    finally:
        driver.close()
        driver.quit()
        return "Authenticated"


def auth(account_id):
    try:
        queue = Queue()
        print("Step 1")
        process = Process(target=auth_process, args=(queue, account_id))
        print("Step 2")
        process.start()
        print("Step 3")
        process.join()  # Wait for the process to finish
        print("Step 4")
        result = queue.get()  # Get the result from the process
        print("Step 5")

        return result
    except Exception as e:
        print("Error authenticating auth:", str(e))
        raise e
