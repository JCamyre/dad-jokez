from pymongo import MongoClient
from settings import mongo_connection_string

client = MongoClient(mongo_connection_string)
db = client.subs


def add_to_sub_list(phone_number: str):
    sub = {
        'number': phone_number
    }

    result = db.sub_list.insert_one(sub)
    print(f'Add one sub as {result.inserted_id}')


def remove_from_sub_list(phone_number: str):
    sub = {
        'number': phone_number
    }
    db.sub_list.delete_one(sub)
    print(f'Removed one sub from db')


def does_number_exist(phone_number: str):
    search_count = len(
        [sub for sub in db.sub_list.find({'number': phone_number})])
    return search_count > 0
