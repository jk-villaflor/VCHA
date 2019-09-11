import nltk  # Load NLTK
import time
from service.TextMiningService import TextMiningService
from service.sklearnService import SkLearnService
from service.propertyService import PropertyService
from collections import defaultdict

# nltk.download()

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from db.postgresl import PropertyDAO
from model.Property import Property

propertyDao = PropertyDAO()
propertyService = PropertyService()
sklearnService = SkLearnService()
textMiningService = TextMiningService()

rows = propertyDao.getRecordsWithNoLocation();

print("Records: ", len(rows)) 
records = []

for row in rows:
    records.append(Property(row[0], row[1].encode("utf-8"), row[2], row[3], row[4]))

size = len(rows)
count = 0
result = defaultdict(list)
for property in records:
    property = propertyService.populateRoomSize(property)
    sentences = propertyService.getSentences(str(property.description))
    property.setLocation(propertyService.getLocationFromSentences(sentences, property.link))   
    if len(property.location) > 0:
        result[property.location].append(property.id)
    print(property.id, ' - location: ', property.location)
    #propertyDao.updateRecord(property)
    count += 1
    try:
        if count % 300 == 0:
            percent = round((count / size * 100), 2);
            print('==========================================')
            print('PROGESS: ', count, '/', size, '(', percent, '%)')
            print('==========================================')
            time.sleep(1)
    except:
           print("error showing the progress")

print(count,' records processed.')
    
for key in result.keys():
    print(key,':',result[key])
    propertyDao.updateLocationRecord(key, result[key])
    
print('Properties location updated!')
