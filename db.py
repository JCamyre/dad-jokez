from pymongo import MongoClient
from settings import mongo_connection_string

client = MongoClient(mongo_connection_string)
db = client.subs


def add_to_sub_list(phone_number: str):
    sub = {"number": phone_number}

    result = db.sub_list.insert_one(sub)
    print(f"Add one sub as {result.inserted_id}")


def remove_from_sub_list(phone_number: str):
    sub = {"number": phone_number}
    db.sub_list.delete_one(sub)
    print(f"Removed one sub from db")


def does_number_exist(phone_number: str):
    search_count = len([sub for sub in db.sub_list.find({"number": phone_number})])
    return search_count > 0

def does_joke_exist(joke: str):
    joke_count = len([joke for joke in db.joke_list.find({"joke": joke})])
    return joke_count > 0

def add_joke_to_db(daily_joke: str):
    daily_joke = {"joke": daily_joke}

    result = db.joke_list.insert_one(daily_joke)
    print(f"Added one joke as {result.inserted_id}")
