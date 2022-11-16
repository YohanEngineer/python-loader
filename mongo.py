from encodings import utf_8
from pydoc import doc
import pymongo
import os
import json


USER = os.getenv('MONGO_USER')
PASSWORD = os.getenv('MONGO_PASSWORD')

# MONGO_URL = 'mongodb://{}:{}@192.168.1.21:27017'.format(USER,PASSWORD)
MONGO_URL = 'mongodb+srv://{}:{}@cluster0.limnd9j.mongodb.net/?retryWrites=true&w=majority'.format(USER,PASSWORD)


try:
    client = pymongo.MongoClient(MONGO_URL,
        connectTimeoutMS=30000,
        socketTimeoutMS=None)
    print("Connection successful")
except:
    print("Unsuccessful connection")



# client.drop_database('quran')
# client.drop_database('quran_fr')
db=client.quran_fr


def ingestion_process():


    list_of_surah_name = []

    #Retrieve Quran chapters 
    chapters = open('F:/Documents/Documents/VS-projects/python-etl/resources/index.json','r',encoding='utf-8')

    #Loading the json inside the surah_name variable
    surah_name = json.load(chapters)

    #Getting each surah transliteration
    for surah in surah_name:
        list_of_surah_name.append((surah['transliteration'], surah['id']))


    for surah in list_of_surah_name:
        print('Creating collection {}'.format(surah[0]))
        db.create_collection(surah[0])
        document = {'number' : surah[1], 'translation': surah[0]}
        db.summary.insert_one(document)

    #Retrieve Quran chapters with translation 
    data = open('F:/Documents/Documents/VS-projects/python-etl/resources/quran_fr.json','r',encoding='utf-8')


    surah_data = json.load(data)

    for surah in surah_data:
        if surah['transliteration'] in [name[0] for name in list_of_surah_name]:
            collection = surah['transliteration']
            print('Inserting in collection {}'.format(surah['transliteration']))
            verses = surah['verses']
            documents = []
            for verse in verses:
                aya_number = verse['id']
                translation = verse['translation']
                document = {'aya_number' : aya_number, 'translation': translation}
                documents.append(document)
            db.get_collection(collection).insert_many(documents)


ingestion_process()
