import pymongo
import requests
import settings
import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

print(settings.DATABASE_NAME)

client = pymongo.MongoClient(settings.MONGO_URI)
vcha_db = client.VCHA
vcha_col = vcha_db.extracted_data
values=vcha_col.find_one({'house_no':1})

print(re.sub("[^\w]"," " ,values['house_description']).split())

#for value in values:
#    print(value)