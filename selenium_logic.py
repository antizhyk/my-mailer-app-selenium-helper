from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import time



s = Service(executable_path="/home/dev/myProjects/selenium_helper/chromedriver-linux64/chromedriver")


def create_driver(proxy=None, agent=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")

    if agent:
        options.add_argument(f"user-agent={agent}")

    seleniumwire_options = {}

    if proxy:
        seleniumwire_options = {
            'proxy': {
                'http': proxy,
                'verify_ssl': False,
            },
        }

    driver = webdriver.Chrome(service=s, seleniumwire_options=seleniumwire_options, options=options)




    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;

      '''
    })
    return driver


def test_driver():
    driver = create_driver()
    try:
        driver.maximize_window()
        driver.get("https://www.google.com/")
        time.sleep(60)
    except Exception as e:
        print("Ошибка:", str(e))
    finally:
        driver.close()
        driver.quit()
        print("Закрыл драйвер")
