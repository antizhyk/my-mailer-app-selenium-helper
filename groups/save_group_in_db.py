import json
import re
from bson import ObjectId
from db import db


def save_groups_in_db(account_id):
    try:
        groups_from_db = list(db['chats'].find({'account': ObjectId(account_id)}, sort=[("position", 1)]))
        # get last position from groups_from_db by key 'position'
        position = 0

        if groups_from_db:
            for group in groups_from_db:
                # check if exist group['position']
                if 'position' in group and group['position'] is not None and group['position'] > position:
                    position = int(group['position'])
        else:
            groups_from_db = []

        with open(f'conversations_{account_id}.json', 'r') as f:
            groups_from_file = json.load(f)

        #     run cicle for groups_from_file
        for group in groups_from_file:
            exist_group = None
            print("group^ ", group['conversation_id'])
            for group_db in groups_from_db:
                # print("ids^ ", group['conversation_id'], group_db['twitterId'])
                print("ids^ ", group['conversation_id'], group_db['twitterId'])
                if group['conversation_id'] == group_db['twitterId']:
                    exist_group = group_db
                    break

            if not exist_group:
                position += 1
                repostCount = get_count(group['name'])
                db['chats'].insert_one({
                    'account': ObjectId(account_id),
                    'position': position,
                    'twitterId': group['conversation_id'],
                    'name': group['name'],
                    'participantsCount': group['participants_count'],
                    'repostCount': repostCount
                })
            else:
                exist_group['name'] = group['name']
                exist_group['participantsCount'] = group['participants_count']
                db['chats'].update_one({'_id': exist_group['_id']}, {"$set": exist_group})

        for group_db in groups_from_db:
            exist_group = None
            for group in groups_from_file:
                if group['conversation_id'] == group_db['twitterId']:
                    exist_group = group
                    break
            if not exist_group:
                db['chats'].delete_one({'_id': group_db['_id']})
    except Exception as e:
        print("Error saving groups in db:", str(e))
        raise e


def get_count(text):
    regex = re.compile(r'(\d+/\d+)')
    match = regex.search(text)
    result = int(match.group(0).split('/')[1]) if match else 0

    if result > 5:
        result = 5

    return result
