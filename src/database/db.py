# db.py
from pymongo import MongoClient
from config.settings import MONGODB_SETTINGS

def get_connection():
    host = MONGODB_SETTINGS['HOST']
    port = MONGODB_SETTINGS['PORT']
    db_name = MONGODB_SETTINGS['DB_NAME']
    
    if 'USER' in MONGODB_SETTINGS and 'PASSWORD' in MONGODB_SETTINGS:
        username = MONGODB_SETTINGS['USER']
        password = MONGODB_SETTINGS['PASSWORD']
        uri = f'mongodb://{username}:{password}@{host}:{port}/{db_name}'
        connection = MongoClient(uri)
    else:
        uri = f'mongodb://{host}:{port}/{db_name}'
        connection = MongoClient(uri)

    return connection[db_name]
