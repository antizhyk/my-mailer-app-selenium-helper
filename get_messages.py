import gzip
import json
import time
import os
from bson import ObjectId
from selenium.common import NoSuchElementException, WebDriverException

from check_auth import check_auth
from cookies_conversion import driver_cookie_conversion
from db import db
from groups.save_group_in_db import save_groups_in_db
from selenium_logic import create_driver


def remove_duplicate_conversations(account_id, file_path=None):
    if file_path is None:
        file_path = f'conversations_{account_id}.json'
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"No file found at {file_path} to remove duplicates from.")
        return

    # Read the existing data
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            conversations = json.load(file)
            # Ensure existing data is a list
            if not isinstance(conversations, list):
                print("The file content is not a list of conversations.")
                return
        except json.JSONDecodeError:
            print("Error reading the JSON file.")
            return

    # Create a dictionary to hold unique conversations
    unique_conversations = {}
    for conv in conversations:
        # Use conversation_id as the key to ensure uniqueness
        unique_conversations[conv['conversation_id']] = conv

    # Get the list of unique conversations
    unique_conversations_list = list(unique_conversations.values())

    # Write the unique conversations back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_conversations_list, file, ensure_ascii=False, indent=4)

    print(f"Removed duplicates. The file now contains {len(unique_conversations_list)} unique conversations.")


def save_conversations_to_file(conversations, account_id, file_path=None):
    if file_path is None:
        file_path = f'conversations_{account_id}.json'

    # Check if the file already exists
    if os.path.exists(file_path):
        # Read the existing data
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
                # Ensure existing data is a list
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Transform the conversations to only include "conversation_id", "name", and the length of "participants"
    transformed_conversations = [
        {
            'conversation_id': conv.get('conversation_id'),
            'name': conv.get('name'),
            'participants_count': len(conv.get('participants', []))
        }
        for conv in conversations
    ]

    # Append the transformed conversations to the existing data
    existing_data.extend(transformed_conversations)

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def decode_response_body(body):
    try:
        # Try to decode as regular utf-8 string
        return body.decode('utf-8')
    except UnicodeDecodeError:
        # If utf-8 decoding fails, try decompressing as gzip
        try:
            return gzip.decompress(body).decode('utf-8')
        except OSError:
            # If decompression fails, raise an error
            raise Exception("Could not decode response body.")


def extract_conversations_from_body(decoded_body):
    try:
        body_json = json.loads(decoded_body)
        # Initialize an empty list to hold the filtered conversations
        filtered_conversations = []
        # Check for the first path
        conversations = body_json.get('user_events', {}).get('conversations')
        if conversations:
            filtered_conversations.extend(conversations.values())
        # Check for the second path
        conversations = body_json.get('inbox_initial_state', {}).get('conversations')
        if conversations:
            filtered_conversations.extend(conversations.values())
        # Filter conversations where "type" is "GROUP_DM"
        group_dm_conversations = [
            conv for conv in filtered_conversations if conv.get('type') == 'GROUP_DM'
        ]
        return group_dm_conversations
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", str(e))
        raise e


def get_messages(account_id):
    driver = None
    try:

        account = db['accounts'].find_one({'_id': ObjectId(account_id)})

        account_config = db['accountconfigs'].find_one({'_id': ObjectId(account["accountConfig"])})
        cookies_from_db = account_config['fullCookies']
        parsed_cookies = driver_cookie_conversion(cookies_from_db)
        print("Parsed cookies:", parsed_cookies)
        proxy_url = None
        if 'proxy' in account and account['proxy'] is not None:
            proxy = db['proxies'].find_one({'_id': ObjectId(account["proxy"])})
            print("proxy:", proxy)
            proxy_url = f"http://{proxy['login']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
        if account_config and 'userAgent' in account_config:
            agent = account_config['userAgent']
        else:
            agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.71 Safari/537.36"

        driver = create_driver(proxy_url, agent)

        driver.get("https://twitter.com")

        for cookie in parsed_cookies:
            driver.add_cookie(cookie)

        driver.get("https://twitter.com/messages")
        time.sleep(30)  # This is a simple wait, you might want to use WebDriverWait for better results
        is_auth = check_auth(driver, "https://twitter.com/messages")

        print("is_auth:", is_auth)

        if is_auth is False:
            print("Not authenticated")
            raise Exception("Not authenticated")
        for request in driver.requests:
            if request.response:
                if "dm/user_updates.json" in request.url or "dm/inbox_initial_state.json" in request.url:
                    print("Request URL:", request.url)
                    body = request.response.body
                    try:
                        decoded_body = decode_response_body(body)
                        conversations = extract_conversations_from_body(decoded_body)
                        if conversations:
                            print("Filtered GROUP_DM Conversations found:")
                            # Save the conversations to a file
                            save_conversations_to_file(conversations, account_id)
                        else:
                            print("No GROUP_DM conversations found in the response.")
                        # Now you can process the conversations as needed
                    except Exception as e:
                        print("Error processing response body:", str(e))
                        raise e
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            for request in driver.requests:
                if request.response:
                    if "dm/user_updates.json" in request.url or "dm/inbox_initial_state.json" in request.url:
                        print("Request URL:", request.url)
                        body = request.response.body
                        try:
                            decoded_body = decode_response_body(body)
                            conversations = extract_conversations_from_body(decoded_body)
                            if conversations:
                                print("Filtered GROUP_DM Conversations found:")
                                # Save the conversations to a file
                                save_conversations_to_file(conversations, account_id)
                            else:
                                print("No GROUP_DM conversations found in the response.")
                            # Now you can process the conversations as needed
                        except Exception as e:
                            print("Error processing response body:", str(e))
                            raise e
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new messages to load
            time.sleep(5)  # Adjust time as necessary

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # Call the function to remove duplicates
        remove_duplicate_conversations(account_id)
        save_groups_in_db(account_id)
    except json.JSONDecodeError as e:
        print("JSON format error in cookies.json:", str(e))
        with open('cookies.json', 'r') as f:
            print("Content of cookies.json:", f.read())
        raise e
    except NoSuchElementException as e:
        print("Container not found:", str(e))
        raise e
    except WebDriverException as e:
        print("WebDriver error:", str(e))
        raise e
    except Exception as e:
        print("Error getting messages:", str(e))
        raise e
    finally:
        # Close the browser at the end of execution
        if driver:
            driver.quit()
        return "Messages retrieved"