import nltk  # Load NLTK
# nltk.download()

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from db.postgresl import PropertyDAO
from model.Property import Property
from service.TextMiningService import TextMiningService

propertyDao = PropertyDAO()
textMiningService = TextMiningService()

rows = propertyDao.getRecords(500);
#rows = propertyDao.getRecord(6829944535);

print("Records: ", len(rows)) 
records = []

for row in rows:
    records.append(Property(row[0], row[1].encode("utf-8")))
    
text = ""

print ("\nShow me the first 5 records: ", "\n")
for x in range (0, len(rows)):
    text += str(records[x].description) + "\n"
    if x < 5:
        print("Id: ", records[x].id , " Desc: ", records[x].description)

# remove special characters
text = textMiningService.removeSpecialCharacters(text)

tokenized_text = textMiningService.getSentenceTokenize(text)
print(tokenized_text)

tokenized_word = textMiningService.getWordTokenize(text)
print(tokenized_word)

# transform words in lower
tokenized_word = textMiningService.normalizeWordsLower(tokenized_word)
tokenized_word = textMiningService.mergeNegativeWords(tokenized_word)
print("Tokenized Words (lower, negative merge)",tokenized_word)

# frequency
fdist = textMiningService.getFrequencyDist(tokenized_word)

most_common = textMiningService.getMostCommonWords(fdist, 5)
print("\n\nMost Common:", most_common)

# Frequency Distribution Plot
#textMiningService.plotFreqDist(fdist)

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
print("Lemmatized Word:", textMiningService.getLemm('parking','v'))
print("Stemmed Word:", textMiningService.getStemming('parking'))

# Lemmatization
lemmat_words = textMiningService.getLemmatWords(filtered_sent)
lemmat_words = textMiningService.getFilteredSentence(lemmat_words, stop_words)
print("Lemmatization Sentence:", lemmat_words)

fdist = textMiningService.getFrequencyDist(lemmat_words)
most_common = textMiningService.getMostCommonWords(fdist, 15)
# frequency
print("\n\nMost Common:", most_common)    