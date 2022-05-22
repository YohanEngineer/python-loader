from pymongo import MongoClient
import os


USER = os.getenv('MONGO_USER')
PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_URL = 'mongodb://{}:{}@192.168.1.21:27017'.format(USER,PASSWORD)

client = MongoClient(MONGO_URL)
db=client.quran