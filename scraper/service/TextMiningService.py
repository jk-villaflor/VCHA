# NLTK Analysis
import re
import token

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import word_tokenize

import matplotlib.pyplot as plt


# search for negative words association
class TextMiningService:

    # get text without special characters
    def removeSpecialCharacters(self, text):
        return re.sub(r"[^a-zA-Z0-9]+", ' ', text)
    
    def removeNonAlpha(self, words):
        return [word for word in words if (" " in word or word.isalpha()) ]
    
    # get text tokenized
    def getSentenceTokenize(self, text):
        return sent_tokenize(text)
    
    # get text tokenized by words
    def getWordTokenize(self, text):
        return word_tokenize(text)
    
    # transform words in lower
    def normalizeWordsLower(self, words):
        for x in range(0, len(words)):
            words[x] = words[x].lower().strip()
        return words
    
    # get frequency distribution of words
    def getFrequencyDist(self, words):
        return FreqDist(words)
    
    # get most common words from a frequency distribution 
    def getMostCommonWords(self, fdist, qty):
        return fdist.most_common(qty)
    
    def plotFreqDist(self, fdist):
        fdist.plot(30, cumulative=False)
        plt.show()
        
    def mergeNegativeWords(self, tokens):
        associationWordsBefore = ["not", "no"]
        associationWordsAfter = ["allowed", "absolutely", "parking"]
        associationWordsBetween = ["view" , "views"]
        result = []
        r=0
        for i in range(0, len(tokens)):
            if(tokens[i] in associationWordsBefore and i < len(tokens)):
                tokens[i + 1] = tokens[i] + " " + tokens[i + 1];
            elif(tokens[i] in associationWordsAfter and i > 0):
                result[r-1] = tokens[i - 1] + " " + tokens[i];
            elif(tokens[i] in associationWordsBetween and i > 0):
                result[r-1] = tokens[i - 1] + " " + tokens[i] + " " + tokens[i + 1]
                i=i+1;
            else:
                result.append(tokens[i])
                r = r+1
                
        
        return result
        
    def getEnglishStopWords(self):
        words = set(stopwords.words("english"))
        words.add('the')
        words.add('and')
        words.add('vancouver')
        words.add('room')
        words.add('b')
        words.add('qr')
        words.add('code')
        words.add('link')
        words.add('one')
        words.add('contact')
        words.add('suite')
        words.add('post')
        words.add('bedroom')
        words.add('available')
        words.add('info')
        words.add('please')
        words.add('new')
        words.add('rent')
        words.add('show')
        words.add('building')
        words.add('living')
        words.add('floor')
        words.add('house')
        words.add('kitchen')
        words.add('bathroom')
        words.add('area')
        words.add('property')
        words.add('street')
        words.add('south')
        words.add('feature')
        words.add('west')
        words.add('centre')
        words.add('include')
        words.add('com')
        words.add('rental')
        words.add('north')
        words.add('home')
        words.add('list')
        words.add('http')
        words.add('uniqueaccommodations')
        words.add('bedrooms')
        words.add('unit')
        words.add('location')
        words.add('information')
        words.add('shop')
        words.add('full')
        words.add('large')
        words.add('city')
        words.add('bathrooms')
        return words
    
    # get filtered sentence from tokenized words and stop words
    def getFilteredSentence(self, tokenized_word, stop_words):
        filtered_sent = []
        for w in tokenized_word:
            if w not in stop_words:
                filtered_sent.append(w)
                
        return filtered_sent
    
    # get Stemmed words from filtered sentence
    def getStemmedWords(self, filtered_sent):
        ps = PorterStemmer()
        stemmed_words = []
        for w in filtered_sent:
            stemmed_words.append(ps.stem(w))
            
        return stemmed_words

    # get Lemmatization words from filtered sentence
    def getLemmatWords(self, filtered_sent):
        ps = PorterStemmer()
        result_words = []
        for w in filtered_sent:
            result_words.append(self.getLemm(w, 'v'))
            
        return result_words
    
    def getStemming(self, word):
        stem = PorterStemmer()
        return stem.stem(word)
    
    def getLemm(self, word, tag):
        lem = WordNetLemmatizer()
        return lem.lemmatize(word, tag)