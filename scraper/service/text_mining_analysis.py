import nltk  # Load NLTK

#nltk modules
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


#imports
from service.TextMiningService import TextMiningService
from service.sklearnService import SkLearnService
from db.postgresl import PropertyDAO
from model.Property import Property

#data access object for properties stored in database
propertyDao = PropertyDAO()

#sklearn implemented services for our use case
sklearnService = SkLearnService()

#nltk implemented services for our use case
textMiningService = TextMiningService()

records = []
descriptions = [];


rows = propertyDao.getRecords(1000); #fetch rows from database
#rows = propertyDao.getRecord(6829944535); #fecth one record from database

print("Records: ", len(rows)) #print amount of rows returned 

#load database rows into property objects and store into records array
for row in rows:
    records.append(Property(row[0], row[1].encode("utf-8"), row[2]))

text = ""

print ("\nShow me the first 5 records: ", "\n")
for x in range (0, len(rows)):
    descriptions.append(str(records[x].description))
    if x < 5:
        print("Id: ", records[x].id , " Desc: ", records[x].description)

# remove special characters
for i in range(0,len(descriptions)):
    descriptions[i] = textMiningService.removeSpecialCharacters(descriptions[i])

# transform words in lower
descriptions = textMiningService.normalizeWordsLower(descriptions)

sentences = []
cleanSentence = ["xe2","www","http","link", "code","post","this","info","contact","to","the","rent",
                 "vancouver bc","lease","at show","in suite","call show","will be","in vancouver","per month"
                 ,"sq ft", "no pets no","we do","is not","and no","with an","as well","you can","that we","is located"
                 ,"from sources","obtained from","you have","for your", "rates and", "does not", "we have", "can be","is subject"
                 ,"and more","british columbia",'it is',"visit our","of our","owner of","if you","your personal","timing","or text"
                 ,"has been","and all","you will","apply or","contained herein","1st 2019","well as","how many","in your","such as"
                 ,"prospective tenants","but we","you are","set up","x80","x93","v6b","sources","com listing","xc2",'all properties'
                 ,"properties listed","or processing","terms and","specific location","1020","an agent","com vancouver",'and credit'
                 ,"is your","be considered","we deem","us by","property or",'its accuracy',"deem reliable","handling fees"
                 ,"application fees","any handling","com disclaimer","quick reference","be verified","have any","are all"
                 ,"not guaranteed","not charge","check required","processing fees","four questions","bathrm","pets what",'us are','officeunique real'
                 ,'side','only available'
                 ]
cleanExact = ["bedrooms bedroom","bedroom bathroom", "bedrooms bathrooms", "kitchen with","walk in", "available for", "move in","not included","for more",
              "do not","one year","located in", "stainless steel","stainless steel appliances","managed by" ,"full property"
              ,"street vancouver","high end","room and", "vancouver and","no smoking no",'heart of','and dryer','washer and'
              ,'management services','are subject', 'sorry no','pets no smoking','open concept','property is','is not'
              ,'views of','one bedroom','built in','room with','of vancouver','master bedroom','lots of','available march','looking for'
              'kitchen and','available april','away from','credit check','in closet','one of','an appointment','included in','smoking no pets'
              ,'and hot','looking for','kitchen and','perfect for','our website','for viewing','visit our','heat and','april 1st','and hot water'
              ,'living room','living area','living space','square feet','move out','your private','suite with', 'in unit', 'suite is'
              ,'on site','natural light','restaurants and','bedroom with','bedroom and','bedrooms and','term minimum','absolutely no'
              ,'comes with','water and','is available','appliances and','march 1st','and west','availability rates','plenty of'
              ,'half month','and large','month available','apartments for','equipped with','located at','housing type','not all','suite in'
              ,'full size','main floor','located on','shops and','park and','or visit','or view','floor plan','property with'
              ,'and full','have no','many people','and dining','fees or','accuracy but we','or obtained','doubt its accuracy'
              ,'vancouver property','guarantee it','estate services','book an appointment','vancouver listings','us or view'
              ,'have no reason','bright and','minimum one','minutes away','and bathroom','just steps','phone show','and is'
              ,'and availability','with large','april 2019','are not','vancouver furnished','live in','and shopping','of natural'
              ,'is an','do you','and restaurants','email show','property details','book an','it furnished','us or','24 hour','with us','1010 west'
            ];
              
cont=0
for i in range(0,len(descriptions)):
    sentence = sklearnService.getSentenceFromText(descriptions[i], 2, 3)
    for s in sentence:
        addS = True
        if any(c in s for c in cleanSentence):
            addS = False
        if addS == True and any(c == s for c in cleanExact):
            addS = False
        
        if addS:
            sentences.append(s)
        

sentences = sklearnService.filterSameMeaning(sentences)

print("Sentences: ",sentences)


# using nltk service to get frequency distribution for our found sentences
fdist = textMiningService.getFrequencyDist(sentences)
most_common = textMiningService.getMostCommonWords(fdist, 200)
print("\n\nMost Common:")
i=1
for common in most_common:
    print(str(i)," - ", common)
    i=i+1
