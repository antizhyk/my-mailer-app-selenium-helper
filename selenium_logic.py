from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import seleniumwire.undetected_chromedriver as uc
import time

# s = Service(executable_path="/root/selenium_helper/chromedriver-linux64/chromedriver")
s = Service(executable_path="/home/dev/myProjects/selenium_helper/chromedriver-linux64/chromedriver")


def create_driver(proxy=None, agent=None):
    print("Creating driver", uc)
    extension_capsolver_file_path="/home/dev/myProjects/selenium_helper/capsolver"
    # options = webdriver.ChromeOptions()
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--no-sandbox')
    options.add_argument('--no-zygote')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-breakpad')
    options.add_argument(f"--load-extension={extension_capsolver_file_path}")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")
    # options.add_extension(extension_capsolver_file_path)

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

    driver = uc.Chrome(service=s, seleniumwire_options=seleniumwire_options, options=options)

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
        driver.get("https://2ip.ua/ru/")
        time.sleep(30)
        # get id="formStuff" and slow scroll to it
        form_stuff = driver.find_element(By.ID, "formStuff")
        # driver.execute_script("arguments[0].scrollIntoView();", form_stuff)
        ActionChains(driver).move_to_element(form_stuff).perform()
        time.sleep(2)
        name = driver.find_element(By.XPATH, '//input[@name="userName"]')
        name.clear()
        name_str = "test"
        for char in name_str:
            name.send_keys(char)
            time.sleep(0.1)

        time.sleep(2)
        mail = driver.find_element(By.XPATH, '//input[@name="eMail"]')
        mail.clear()
        mail_str = "test@test.com"
        for char in mail_str:
            mail.send_keys(char)
            time.sleep(0.1)
        time.sleep(2)
        ActionChains(driver).move_to_element(form_stuff).perform()
        time.sleep(2)
        driver.find_element(By.XPATH, '//input[@name="terms"]').click()
        time.sleep(2)

        driver.find_element(By.XPATH, '//input[@name="radioCat"]')\
            .click()

        driver.find_element(By.XPATH, '//button[@id="submit"]')\
            .click()
        time.sleep(300)
    except Exception as e:
        print("Ошибка:", str(e))
    finally:
        driver.close()
        driver.quit()
        print("Закрыл драйвер")
