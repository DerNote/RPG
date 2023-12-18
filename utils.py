####  
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('url')
client = pymongo.MongoClient(uri)
db = client['RPG']