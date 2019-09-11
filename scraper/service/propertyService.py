import re
from model.Property import Property
from service.TextMiningService import TextMiningService
from service.sklearnService import SkLearnService


class PropertyService:
    
    def populateRoomSize(self, property : Property):
        sp = property.characteristics.split('-')
        for s in sp:
            if s is not None:
                s = str(s)
                if 'br' in s:
                    rooms = s.replace('br', '').strip()
                    property.setRooms(rooms);
                    property.setUpdate()
                elif 'ft_sq' in s:
                    size = s.replace('ft_sq', '').strip()
                    property.setSize(size);
                    property.setUpdate()
        
        return property;
    
    def populateTokens(self, property : Property, sentences):
        searchfor = ['professionally managed', 'no pets', 'parking stall', 'available now', 'building amenities', 'near school', 'brand new', 'suite laundry']
        if sentences is not None:
            for sentence in sentences:
                if sentence in searchfor:
                    property.setToken(sentence)
                 
        return property

    def getLocationFromSentences(self, sentences, link):
        link = link.replace('https://vancouver.craigslist.org/','') 
        locations = ['burnaby', 'new westminster', 'richmond' ,'stanley park', 'surrey', 'vancouver', 'downtown', 'abbotsford', 'granville', 'brentwood','delta','langley','white-rock','coquitlam','new-westminster','fleetwood','port-moody']
        
        for location in locations:
            if location in link:
                return location
        
        for location in locations:
            for sentence in sentences:
                if location in sentence:
                    return location;
        return '';
        
    def getSentences(self, description):
        textMiningService = TextMiningService()
        sklearnService = SkLearnService()
        
        description = textMiningService.removeSpecialCharacters(description)
        description = description.lower().strip()
        
        sentences = sklearnService.getSentenceFromText(description, 2, 3);
        sentences = sklearnService.filterSameMeaning(sentences)
        
        return sentences;

    # method to extract number of bedrooms from text
    def tryGetBedroomFromDescription(self, property : Property):
        numbers = ['one', 'two', 'three', 'four', 'five']  # writed numbers to be found
        exact = ['1bd', '2bd', '3bd', '4bd', '5bd']  # numbers with bd together pattern
        exact2 = ['1-br', '2-br', '3-br', '4-br', '5-br']  # numbers with bd together pattern
        exact3 = ['1bed', '2bed', '3bed', '4bed', '5bed']  # numbers with bd together pattern
        
        desc = str(property.title).lower() + ' ' + str(property.description).lower()  # parse the texto to lowercase
        words = desc.split(' ');
        for i in range(0, len(words)):
            if words[i] in exact:  # check for a specific pattern in text and return the exact number of rooms from array position
                r = exact.index(words[i]) + 1
                property.setRooms(r)
                property.setUpdate()
                return property;
           
            if words[i] in exact2:  # check for a specific pattern in text and return the exact number of rooms from array position
                r = exact2.index(words[i]) + 1
                property.setRooms(r)
                property.setUpdate()
                return property;

            if words[i] in exact3:  # check for a specific pattern in text and return the exact number of rooms from array position
                r = exact3.index(words[i]) + 1
                property.setRooms(r)
                property.setUpdate()
                return property;
            
            # check for a split pattern in text and apply algorithm to identify the number
            if words[i] in ['bedroom', 'bedrooms', 'bed', 'br', 'brm', 'bdrm', 'bdr'] or 'bed' in words[i] or 'bd' in words[i]:
                lw = str(words[i - 1]).strip()
                if(lw in numbers):
                    lw = numbers.index(lw) + 1
                r = -1
                try:
                    r = int(lw)
                except:
                    r = -1
                if r == -1:
                    try:
                        r = float(lw)
                    except:
                        r = -1
                if r >= 0 and r <= 7 :  # if the number is too high probably is not right
                    property.setRooms(r)
                    property.setUpdate()
                    return property;
            
            if 'studio' in words or 'bachelor ' in desc or 'bachlor ' in desc:
                property.setRooms(1)
                property.setUpdate()
                return property;
            
        find = re.search("\d{1,5}[b][d]", desc)
        if find:
            size = str(find.group()).replace('bd', '').strip()
            r = -1
            try:
                r = float(size)
                if r >= 0 and r <= 7 :
                    property.setRooms(r)
                    property.setUpdate()
                    return property;
                    
            except:
                r = -1
                
        return property;
    
    def tryGetSizeFromDescription(self, property : Property):
        
        desc = str(property.characteristics).lower() + ' ' + str(property.title).lower() + ' ' + str(property.description).lower()  # parse the texto to lowercase
        words = desc.split(' ');
        for i in range(0, len(words)):
            
            # check for a split pattern in text and apply algorithm to identify the number
            if words[i] in ['square', 'sqft', 'sq.', 'sqt', 'sqf', 'sqft)', 'sq.ft.', 'sqft.', 'sq', 'sqft,', 'sf', 'sq.ft' , 'sq.ft.,' , 'sqft).', 'sq/ft', 'sq.ft'] :
                lw = str(words[i - 1]).strip().replace('+', '').replace(',', '')
                r = -1
                try:
                    r = int(lw)
                except:
                    r = -1
                if r == -1:
                    try:
                        r = float(lw)
                    except:
                        r = -1
                if r >= 100 :
                    property.setSize(r)
                    property.setUpdate()
                    return property;
                
            if words[i] in ['sq/ft:', 'footage:'] :
                lw = str(words[i + 1]).strip().replace('+', '').replace(',', '')
                r = -1
                try:
                    r = int(lw)
                except:
                    r = -1
                if r == -1:
                    try:
                        r = float(lw)
                    except:
                        r = -1
                if r >= 100 :
                    property.setSize(r)
                    property.setUpdate()
                    return property;
        
        find = re.search("\d{1,5}.sq", desc)
        if not find: 
            find = re.search("\d{1,5}.ft", desc)
        if find:
            size = str(find.group()).replace('sq', '').replace('ft', '').strip()
            r = -1
            try:
                r = float(size)
                if r >= 100 :
                    property.setSize(r)
                    property.setUpdate()
                    return property;
                    
            except:
                r = -1
                
        return property;
    
    def tryGetBathFromDescription(self, property : Property):
        numbers = ['one', 'two', 'three', 'four', 'five']  # writed numbers to be found
        desc = str(property.characteristics).lower() + ' ' + str(property.title).lower() + ' ' + str(property.description).lower()  # parse the texto to lowercase
        desc = desc.replace('\\xc2',' ').replace('\\xa0',' ') #clean dirty
        desc = desc.replace('&nbsp;',' ').replace('+', ' ').replace('/', ' ').replace('-', ' ') #clean dirty
        desc = desc.replace('full','').replace('private','').replace('  ',' ') #replace word full there is found between the bathroom word and number
        words = desc.split(' ');
        wordContains = ['bath','bths']
        
        if 'one and half ba' in desc:
            property.setBath(1.5)
            property.setUpdate()
            return property;
        
        find = re.search("\d{1,5}ba|\d[.]\d{1,5}ba", desc)
        if find:
            bath = str(find.group()).replace('ba', '').strip()
            r = -1
            try:
                r = float(bath)
                if r > 0 and  r <= 7 :
                    property.setBath(r)
                    property.setUpdate()
                    return property;
            except:
                pass
        
        # check for a split pattern in text and apply algorithm to identify the number
        for i in range(0, len(words)):
            #check if word has exact pattern to search for number in next word            
            if words[i] in ['bath:','bathroom:', 'bathrooms:', 'bathroom(s):'] :
                lw = str(words[i + 1]).strip().replace('+', '').replace(',', '')
                if(lw in numbers):
                    lw = numbers.index(lw) + 1
                r = -1
                try:
                    r = float(lw)
                    if r > 0 and  r <= 7 :
                        property.setBath(r)
                        property.setUpdate()
                        return property;
                except:
                    pass
            
            #check if word contains pattern to search for number in previous word            
            if any(w in words[i] for w in wordContains ) :
                lw = str(words[i - 1]).strip().replace('+', '').replace(',', '.').replace('/', '')
                if(lw in numbers):
                    lw = numbers.index(lw) + 1
                r = -1
                try:
                    r = float(lw)
                    if r > 0 and  r <= 7 :
                        property.setBath(r)
                        property.setUpdate()
                        return property;
                except:
                    pass
                
        if 'bath' in desc:
            property.setBath(1)
            property.setUpdate()
            return property;
                
        return property;
        
