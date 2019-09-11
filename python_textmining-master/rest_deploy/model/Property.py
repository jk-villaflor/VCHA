import json
class Property:
    def __init__(self, id, description, characteristics, title):
        self.id = id
        self.description = description
        self.characteristics = characteristics;
        self.title = title
        self.tokens = []
        self.rooms = -1
        self.size = -1
        self.bath = -1
        self.profMan = False
        self.nopet = False
        self.suitLaundry = False
        self.parkStall = False
        self.availNow = False
        self.amenities = False
        self.nearSchool = False
        self.brandNew = False
        self.update = False
        
    def getPartDescription(self):
        if len(self.description) > 50:
            return str.join(str(self.description)[:50], " ...")
        else:
            return self.description;
        
    def setLocation(self,location):
        self.location = location
        
    def setRooms(self, rooms):
        self.rooms = rooms;

    def setBath(self, bath):
        self.bath = bath;

    def setUpdate(self):
        self.update = True;
 
    def setSize(self, size):
        self.size = size;
    
    def setToken(self,token):
        if(token not in self.tokens):
            self.tokens.append(token)
        
        if token == 'professionally managed':
            self.profMan = True
        elif token == 'no pets':
            self.nopet = True
        elif token == 'suite laundry':
            self.suitLaundry = True
        elif token == 'parking stall':
            self.parkStall = True
        elif token == 'available now':
            self.availNow = True
        elif token == 'building amenities':
            self.amenities = True
        elif token == 'near school':
            self.nearSchool = True
        elif token == 'brand new':
            self.brandNew = True
            
    def getJson(self):
        data = {'id':self.id}
        data.update({'title':self.title})
        data.update({'characteristics':self.characteristics})
        data.update({'description':self.getPartDescription()})
        return json.dumps(data)