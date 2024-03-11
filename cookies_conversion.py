import json


def driver_cookie_conversion(cookies_from_db):
    try:
        with open('sameSite.json', 'r') as f:
            same_site_template = json.load(f)

        cookies = []

        for cookie in cookies_from_db:
            print("cookie:", cookie)
            for same_site in same_site_template:
                if same_site['name'] == cookie['name']:
                    cookie['sameSite'] = same_site['sameSite']
                    break
                else:
                    cookie['sameSite'] = "None"

            cookies.append(cookie)
        return cookies
    except Exception as e:
        print("Error:", str(e))
        raise e
