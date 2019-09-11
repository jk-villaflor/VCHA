import nltk  # Load NLTK
import time
from service.TextMiningService import TextMiningService
from service.sklearnService import SkLearnService
from service.propertyService import PropertyService
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

rows = propertyDao.getNoBathRecords(20000);
#rows = propertyDao.getRecord('6829979395');

print("Records: ", len(rows)) 
records = []

for row in rows:
    records.append(Property(row[0], row[1].encode("utf-8"), row[3], row[2]))

size = len(rows)
count = 0
for property in records:
    property = propertyService.tryGetBathFromDescription(property) 
    if property.update == True:
        print(property.id, ' - baths: ', property.bath)
        propertyDao.updateBathRecord(property)
    count += 1
    try:
        if count % 50 == 0:
            percent = round((count / size * 100), 2);
            print('==========================================')
            print('PROGESS: ', count, '/', size, '(', percent, '%)')
            print('==========================================')
            time.sleep(3)
    except:
           print("error showing the progress")
           
print('Finished process: ',size,' records')

