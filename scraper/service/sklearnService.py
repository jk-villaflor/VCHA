#pip install sklearn
from sklearn.feature_extraction.text import TfidfVectorizer


class SkLearnService:

    def getSentenceFromText(self,text,wordsInSentenceFrom,wordsInSentenceTo):
        corpus = []
        corpus.append(text)
        vectorizer = TfidfVectorizer(ngram_range=(wordsInSentenceFrom,wordsInSentenceTo))
        vectorizer.fit_transform(corpus)
        return vectorizer.get_feature_names();
            
    def filterSameMeaning(self, sentences):
        for i in range(0,len(sentences)):
            if sentences[i] == 'pets no' or sentences[i]=='sorry no pets' or sentences[i]=='no pet':
                sentences[i] = 'no pets'
            elif sentences[i] == 'smoking no' or sentences[i] == 'absolutely no smoking':
                sentences[i] = 'no smoking'
            elif sentences[i] == 'professionally managed by' or sentences[i]=='real estate' or sentences[i]=='property management services' or sentences[i] == 'property management' or sentences[i]=='full property management':
                sentences[i] = 'professionally managed'
            elif sentences[i] == 'stainless steel':
                sentences[i] = 'steel appliances'
            elif sentences[i] == 'washer dryer' or sentences[i] == 'washer and dryer':
                sentences[i] = 'suite laundry'
            elif sentences[i] == 'available immediately':
                sentences[i] = 'available now'
            elif sentences[i] == 'suite washer':
                sentences[i] = 'suite laundry'
            elif sentences[i] == 'hardwood flooring':
                sentences[i] = 'hardwood floors'
            elif sentences[i] == 'pet friendly':
                sentences[i] = 'pets allowed'
            elif sentences[i] == 'canada line':
                sentences[i] = 'skytrain station'
            elif sentences[i] == 'furnished realty':
                sentences[i] = 'fully furnished'
            elif sentences[i] == 'secondary school' or sentences[i] == 'private school' or sentences[i] == 'secondary schools' or sentences[i] == 'elementary school' or sentences[i] == 'near school' or sentences[i] == 'near schools' :
                sentences[i] = 'near school'
            elif sentences[i] == 'underground parking' or sentences[i]=='parking available':
                sentences[i] = 'parking stall'
            elif sentences[i] == 'amenities include' or sentences[i]=='all amenities':
                sentences[i] = 'building amenities'
                
        return sentences;

    def test(self, params):
        corpus = [
            "QR Code Link to This Post Property Address: 2566 Marine Drive, West Vancouver, BC V7V 1L4 The House is Professionally Managed By Vista Realty Ltd. An upscale luxury piece of exceptional home with the best workmanship and quality unto the market. It\xe2\x80\x99s brand new and it\xe2\x80\x99s proximity to truly unspoiled waterfront but in touch of the world \xe2\x80\x93 Dundarave Village! AVAILABLE: NOW PROPERTY INFORMATION: Bedrooms: 5 Bathrooms: 3 Chef\xe2\x80\x99s Kitchen: 1 Wok Kitchen: 1 Living Room: 1 Family Room: 1 Home Office 1 Recreation Room: 1 Game Room: 1 Finished area: 4,598 sq.ft. Lot Size: 8,909 sq.ft. Amenities: Landscaped courtyard gardens, Family Room, Living Room, Rec Room, Dundarave Village, the seawall and the beach WHY LIVE IN WEST VANCOUVER \xe2\x80\x93 DUNDARAVE: WALK EVERYWHERE! Dundarave Village just at door steps with shops, restaurants, public transits lined along the streets. This is a great opportunity to have this brand new custom-made house situated at the heart of West Vancouver in the distinctive Dundarave Village. Convenient to everywhere: Highway #1, Lions Gate Bridge, Downtown Vancouver core, Snowcapped mountains, Skii Resort. School Catchments: Ecole Pauline Johnson Elementary, Irwin Park Elementary & West Vancouver Secondary Private Schools: Collingwood School & Mulgrave School FEATURES: This custom-made home has stunning open concept meticulously designed and built featuring vaulted vault ceilings and huge skylights for abundant natural light. It is absolutely stunning with grand foyer with souring ceiling and contemporary chandelier opening unto the highest level of quality home. Gorgeous chef's kitchen outfitted with Wolf gas range, appliance package connected to the living room, formal dining room and Wok kitchen. Upstairs boasts an exquisite master bedroom with spa-like bath, huge walk-in closet and lounge area, private balcony full of sunshine. 2 additional bedrooms along the hallway in the top level - all with spacious closets and ensuites; Basement outfitted with wet bar, 2 extra bedrooms with ensuites, recreational room and over-sized family room. The custom millwork with tasteful design and radiant heating throughout. South-facing backyard very private with over-sized deck and lawn great for entertaining. 2 car attached garage. WHEN RENTING: Deposits: half a month security deposit Lease term: minimum 1 year Pets: No Pets Absolutely no smoking please. Credit and Reference check: Required Vista Realty Ltd Office Address: 208-700 Marine Drive North Vancouver, B.C. Canada V7M 1H3 http://www.vistarealty.ca/ Disclaimer: The information contained herein has either been given to us by the owner of the property or obtained from sources that we deem reliable. We have no reason to doubt its accuracy but we do not guarantee it. Rental availability, rates and timing are subject to change. Visit our website for more pictures and details. www.vistarealty.net"
        ]
        
        vectorizer = TfidfVectorizer(ngram_range=(2,3))
        X = vectorizer.fit_transform(corpus)
        sentences = vectorizer.get_feature_names()
        print(vectorizer.get_feature_names())
        #print(X)

    
    def test2(self):
        from nltk import ngrams
        text = "The room has max capacity of 800 people no smoking allowed no children above 12 yr old ..."
        
        pairs = ngrams(text.split(), 3) # change the 2 here to however many words you want in each group
        
        for pair in pairs:
            print(pair)

