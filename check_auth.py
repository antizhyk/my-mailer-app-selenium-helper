def check_auth(driver, part_of_url):
    try:
        if part_of_url in driver.current_url:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking auth:", str(e))
        raise e
