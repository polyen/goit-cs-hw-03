from pymongo import MongoClient
from pymongo.server_api import ServerApi


def db():
    client = MongoClient('mongodb://localhost:27017', server_api=ServerApi('1'))
    data_base = client.book.cats

    return data_base
