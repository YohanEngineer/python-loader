from encodings import utf_8
from pymongo import MongoClient
import os
import json


USER = os.getenv('MONGO_USER')
PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_URL = 'mongodb://{}:{}@192.168.1.21:27017'.format(USER,PASSWORD)

client = MongoClient(MONGO_URL)
client.drop_database('quran')
db=client.quran


list_of_surah_name = []

#Retrieve Quran chapters 
chapters = open('resources/index.json','r',encoding='utf-8')

#Loading the json inside the surah_name variable
surah_name = json.load(chapters)

#Getting each surah transliteration
for surah in surah_name:
    list_of_surah_name.append(surah['transliteration'])


for name in list_of_surah_name:
    db.create_collection(name)

#Retrieve Quran chapters with translation 
data = open('resources/quran_fr.json','r',encoding='utf-8')


surah_data = json.load(data)

for surah in surah_data:
    if surah['transliteration'] == 'Al-Fatihah':
        collection = surah['transliteration']
        verses = surah['verses']
        for verse in verses:
            aya_number = verse['id']
            translation = verse['translation']
            document = {'aya_number' : aya_number, 'translation': translation}
            db.get_collection(collection).insert_one(document)

