import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
# note: requires >>> nltk.download('punkt')
text = "The solution will include LAN, WAN and Firewall. The LAN will include both fixed and wireless"

sents = sent_tokenize(text)
print(sents)
words = [word_tokenize(sent) for sent in sents]
print(words)

from nltk.corpus import stopwords
# note: requires >>> nltk.download('stopwords')
from string import punctuation
customStopWords = set(stopwords.words('english')+list(punctuation))
print(customStopWords)