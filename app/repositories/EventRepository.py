from app.config import database

def filter_events(eventFilters):
    return database.db["Events"].find(eventFilters)