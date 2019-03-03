import nltk
from nltk.tokenize import word_tokenize, sent_tokenize  # note: requires >>> nltk.download('punkt')
from string import punctuation  # builtin punctuation list
from nltk.corpus import stopwords  # note: requires >>> nltk.download('stopwords')
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures  # finding N-Grams
from nltk.stem.lancaster import LancasterStemmer  # Stemming (Close, Closing, Closed = Clos)
from nltk.corpus import wordnet as wn  # note: requires >>> nltk.download('wordnet')
from nltk.probability import FreqDist  # word frequency
from collections import defaultdict  # dictionary with default values
from heapq import nlargest  # find top n largest items by key


def run_tests(text:str):
    print("### SOURCE TEXT:")
    print(text)

    words = tokenize(text)

    wordsWOStopWords = remove_stop_words(text)

    find_ngrams(wordsWOStopWords)

    stemmed_words = stem_words(wordsWOStopWords)
    # find ngrams again with just stems
    find_ngrams(stemmed_words)

    tag_parts_of_speech(words)

    find_synonyms()


def find_synonyms():
    # Disambiguation example
    print("### DISAMBIGUATION - SYNSETS:")
    for ss in wn.synsets('base'):
        print(ss, ss.definition())


def tag_parts_of_speech(words):
    # Parts of Speech (Noun, Verb etc.)
    # note: requires >>> nltk.download('averaged_perceptron_tagger')
    print("### PARTS OF SPEECH:")
    for pos in nltk.pos_tag(words):
        print(pos)
    # note: refer to nltk documentation for the meaning of pos tags (VBN, NNP etc)


def stem_words(words):
    # Stemming
    st = LancasterStemmer()
    stemmedWords = [st.stem(word) for word in words]
    #print("### STEMMED WORDS:")
    #print("Original:", words)
    #print(stemmedWords)
    return stemmedWords


def find_ngrams(wordsWOStopWords):
    # Finding N-grams (words that occur together)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(wordsWOStopWords)
    print("### BIGRAMS:")
    for ngram in sorted(finder.ngram_fd.items()):
        print(ngram)
    # see also nltk.TrigramAssocMeasures


def remove_stop_words(text):
    # removing words that add no meaning
    customStopWords = set(stopwords.words('english') + list(punctuation))
    wordsWOStopWords = [word for word in word_tokenize(text) if word not in customStopWords]
    #print("### WORDS (WITHOUT STOPWORDS):")
    #print(type(wordsWOStopWords), wordsWOStopWords)
    return wordsWOStopWords


def tokenize(text):
    # breaking strings in sentences and words
    sents = sent_tokenize(text)
    print("### SENTENCES:")
    print(type(sents), sents)
    words = [word_tokenize(sent) for sent in sents]
    print("### WORDS per SENTENCES:")
    print(type(words), words)
    return word_tokenize(text)


def disambiguate(text1, text2, term):
    from nltk.wsd import lesk
    print("### DISAMBIGUATION - LESK:")
    sense1 = lesk(word_tokenize(text1),term)
    print(sense1, sense1.definition())

    sense2 = lesk(word_tokenize(text2),term)
    print(sense2, sense2.definition())


def auto_summarise(text:str, n:int) -> list:
    sents = sent_tokenize(text)
    assert n <= len(sents)

    #words = word_tokenize(text.lower())
    words = remove_stop_words(text.lower())
    freq = FreqDist(words)
    ranking = defaultdict(int)

    for i, sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i]+=freq[w]

    top_sent_idxs = nlargest(n, ranking, ranking.get)

    return [(i, ranking[i], sents[i]) for i in sorted(top_sent_idxs)]
