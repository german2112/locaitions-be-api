from app.config import database

def filter_events(eventFilters):
    return database.db["Events"].find(eventFilters)

def insert_event(event):
    return database.db["Events"].insert_one(event)