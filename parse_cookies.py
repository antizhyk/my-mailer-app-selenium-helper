import json


def parse_cookies(cookies):
    try:
        # Load the template from the sameSite.json file
        with open('sameSite.json', 'r') as file:
            template = json.load(file)

        # Create a dictionary for quick lookup
        template_dict = {cookie['name']: cookie['sameSite'] for cookie in template}

        # Loop through the passed cookies and match them to the template
        parsed_cookies = []
        for cookie in cookies:
            same_site = template_dict.get(cookie['name'], "None")
            cookie_with_same_site = cookie.copy()  # Create a copy to preserve the original cookie
            cookie_with_same_site['sameSite'] = same_site
            parsed_cookies.append(cookie_with_same_site)

        return parsed_cookies
    except Exception as e:
        print("Error parsing cookies:", str(e))
        raise e
