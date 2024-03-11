import json

from bson import ObjectId

from db import db
from selenium_logic import create_driver


def get_chats(account_id: str):
    try:
        account = db['accounts'].find_one({'_id': ObjectId(account_id)})

        account_config = db['accountconfigs'].find_one({'_id': ObjectId(account["accountConfig"])})

        proxy = db['proxies'].find_one({'_id': ObjectId(account["proxy"])})

        proxy_url = f"http://{proxy['login']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
        cookies = account_config['cookies']
        print("Cookies:", cookies)
        if account_config and 'userAgent' in account_config:
            agent = account_config['userAgent']
        else:
            agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.71 Safari/537.36"
        with open('cookies.json', 'r') as f:
            cookies_data = json.load(f)
        driver = create_driver(proxy_url, agent)
        # https://twitter.com/404

        #     get cookies from cookies.json
        driver.get("https://twitter.com")
        get_cookies = driver.get_cookies()
        # save in json
        with open('cookies_old.json', 'w') as f:
            json.dump(get_cookies, f)
        for cookie in cookies_data:
            print(cookie)
            driver.add_cookie(cookie)
        driver.get("https://twitter.com/messages")
    except Exception as e:
        print("Error getting chats:", str(e))
        raise e
    finally:
        return "Chats retrieved"
