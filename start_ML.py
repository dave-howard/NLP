from nltk_test.get_web_data import get_articles, get_article_text
from nltk_test.get_docx_data import read_docx, read_docx_folder

url = "http://doxydonkey.blogspot.com/"

#links = []
#get_articles(url, links, 5)

#text = []
#for url in links:
#    for t in get_article_text(url):
#        text.append(t)

text = read_docx_folder("All HLDs")

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

X = vectorizer.fit_transform(text)
print(type(X))
print(X)

from sklearn.cluster import KMeans
# n_clusters = number of clusters/groups we are asking the model to find
# init = method of defining initial centroids (where the clusters start)

km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1, verbose=True)

fit = km.fit(X)  # pass our vectorised (N-Dimensional hypercube) text into the KMeans model

print(type(fit))
print(fit)

import numpy as np
clusters = np.unique(km.labels_, return_counts=True)
print(clusters)
for cluster in clusters:
    print (cluster)


clustered_text = {}
for i, cluster in enumerate(km.labels_):
    oneDocument = text[i]
    if cluster not in clustered_text.keys():
        clustered_text[cluster] = oneDocument
    else:
        clustered_text[cluster] += oneDocument
'''
for i,c in enumerate(clustered_text):
    print("########### CLUSTER",i)
    print(clustered_text[i])
'''

print("###### cluster summary")
cluster_count = {}
for i, cluster in enumerate(km.labels_):
    print(cluster, text[i])
    if cluster not in cluster_count.keys():
        cluster_count[cluster] = 1
    else:
        cluster_count[cluster]+=1

for i in cluster_count.keys():
    print(i, cluster_count[i])

# analyse the words in each cluster...

from nltk.tokenize import word_tokenize, sent_tokenize  # note: requires >>> nltk.download('punkt')
from string import punctuation  # builtin punctuation list
from nltk.corpus import stopwords  # note: requires >>> nltk.download('stopwords')
#from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures  # finding N-Grams
#from nltk.stem.lancaster import LancasterStemmer  # Stemming (Close, Closing, Closed = Clos)
#from nltk.corpus import wordnet as wn  # note: requires >>> nltk.download('wordnet')
from nltk.probability import FreqDist  # word frequency
from collections import defaultdict  # dictionary with default values
from heapq import nlargest  # find top n largest items by key
import nltk

_stopwords = set(stopwords.words('english')+list(punctuation))

keywords = {}
counts = {}

for cluster in range(5):
    word_sent = word_tokenize(clustered_text[cluster].lower())
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    keywords[cluster] = nlargest(100, freq, key=freq.get)
    counts[cluster] = freq

unique_keys = {}
for cluster in range(5):
    other_clusters = list(set(range(5))-set([cluster]))
    #print(other_clusters)
    keys_other_clusters = set(keywords[other_clusters[0]])
    for c in range(1,4):
        keys_other_clusters = keys_other_clusters.union(set(keywords[other_clusters[c]]))
    #print(keys_other_clusters)
    unique = set(keywords[cluster])-keys_other_clusters
    #print(unique)
    unique_keys[cluster] = nlargest(10, unique, key=counts[cluster].get)

for i in unique_keys.keys():
    print(i, unique_keys[i])




# nearest neighbour - Classifying an item
new_document = [" ".join(read_docx("solution.docx"))]

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier()
classifier.fit(X, km.labels_)
# X being our Vectorised list of documents,
# and km.labels_ being our K-Means model

vectorised_document = vectorizer.transform(new_document)

print(vectorised_document)

cluster_num = classifier.predict(vectorised_document)

print ("Document is assigned to theme/cluster", cluster_num)

