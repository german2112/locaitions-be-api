from app.config import database
from typing import List


def insert(payload):
    return database.db["Tags"].insert_one(payload)


def find(filters):
    return database.db["Tags"].find(filters)


def find_distinct(prop_name: str, filters):
    return database.db["Tags"].distinct(prop_name, filters)


def find_by_label_list(labels: List[str]):
    return database.db["Tags"].find({'label': {'$in': labels}}, {"label": 1})


def insert_many(tags):
    return database.db["Tags"].insert_many(tags)
