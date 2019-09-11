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

rows = propertyDao.getNoRoomSizeRecords(20000);

print("Records: ", len(rows)) 
records = []

for row in rows:
    records.append(Property(row[0], row[1].encode("utf-8"), row[2], row[3]))

size = len(rows)
count = 0
for property in records:
    property = propertyService.tryGetBedroomFromDescription(property)
    if property.update == True:
        print(property.id, ' - ', property.rooms, 'bdr ')
        propertyDao.updateRoomRecord(property)
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

