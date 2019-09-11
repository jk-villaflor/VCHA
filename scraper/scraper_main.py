import nltk  # Load NLTK
import pymongo
import requests
import urllib3
from bs4 import BeautifulSoup
import settings
from bson.objectid import ObjectId
import pprint
from scraper.text_mining.house import house
from scraper.text_mining.TextMiningService import TextMiningService

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# url = "https://vancouver.craigslist.org/search/eby/hhh?hasPic=1"

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


print(settings.DATABASE_NAME)

client = pymongo.MongoClient(settings.MONGO_URI)
vcha_db = client.VCHA
vcha_col = vcha_db.extracted_data
rows = vcha_col.find().limit(50)

list_rows = list(rows)

for rows in list_rows:
    print('{0} {1}'.format(rows['house_title'], rows['house_description']))

###################################################

# nltk.download()
textMiningService = TextMiningService()

print("Records: ", len(rows))
records = []

for row in list_rows:
    records.append(house(row[0], row[1].encode("utf-8")))

text = ""

print("\nShow me the first 5 records: ", "\n")
for x in range(0, len(rows)):
    text += str(records[x].house_description) + "\n"
    if x < 10:
        print("Id: ", records[x].id, " Desc: ", records[x].house_description)

# remove special characters
text = textMiningService.removeSpecialCharacters(text)

tokenized_text = textMiningService.getSentenceTokenize(text)
print(tokenized_text)

tokenized_word = textMiningService.getWordTokenize(text)
print(tokenized_word)

# transform words in lower
tokenized_word = textMiningService.normalizeWordsLower(tokenized_word)
tokenized_word = textMiningService.mergeNegativeWords(tokenized_word)
print("Tokenized Words (lower, negative merge)", tokenized_word)

# frequency
fdist = textMiningService.getFrequencyDist(tokenized_word)

most_common = textMiningService.getMostCommonWords(fdist, 5)
print("\n\nMost Common:", most_common)

# Frequency Distribution Plot
textMiningService.plotFreqDist(fdist)

# Stop Words
stop_words = textMiningService.getEnglishStopWords()
print("Stop words:", stop_words)

filtered_sent = textMiningService.getFilteredSentence(tokenized_word, stop_words)
print("Filtered Sentence (remove stop words):", filtered_sent)

# remove remaining tokens that are not alphabetic
filtered_sent = textMiningService.removeNonAlpha(filtered_sent)

print("Filtered Sentence (only alpha):", filtered_sent)

# frequency
fdist = textMiningService.getFrequencyDist(filtered_sent)

most_common = textMiningService.getMostCommonWords(fdist, 15)
print("\n\nMost Common:", most_common)

# Stemming
stemmed_words = textMiningService.getStemmedWords(filtered_sent)
print("Filtered Sentence:", filtered_sent)
print("Stemmed Sentence:", stemmed_words)

# Lexicon Normalization
# performing stemming and Lemmatization
print("Lemmatized Word:", textMiningService.getLemm('parking', 'v'))
print("Stemmed Word:", textMiningService.getStemming('parking'))

# Lemmatization
lemmat_words = textMiningService.getLemmatWords(filtered_sent)
lemmat_words = textMiningService.getFilteredSentence(lemmat_words, stop_words)
print("Lemmatization Sentence:", lemmat_words)

fdist = textMiningService.getFrequencyDist(lemmat_words)
most_common = textMiningService.getMostCommonWords(fdist, 15)
# frequency
print("\n\nMost Common:", most_common)
