import nltk
from nltk.tokenize import word_tokenize, sent_tokenize


def run_tests(text:str, text2:str):
    # note: requires >>> nltk.download('punkt')
    #text = "The solution will include LAN, WAN and Firewall. The LAN will include both fixed and wireless"
    print("### SOURCE TEXT:")
    print(text)

    # breaking strings in sentences and words
    sents = sent_tokenize(text)
    print("### SENTENCES:")
    print(type(sents), sents)
    words = [word_tokenize(sent) for sent in sents]
    print("### WORDS:")
    print(type(words), words)

    # removing words that add no meaning
    from nltk.corpus import stopwords
    # note: requires >>> nltk.download('stopwords')
    from string import punctuation
    customStopWords = set(stopwords.words('english')+list(punctuation))
    #print(customStopWords)
    wordsWOStopWords = [word for word in word_tokenize(text) if word not in customStopWords]
    print("### WORDS (WITHOUT STOPWORDS):")
    print(type(wordsWOStopWords), wordsWOStopWords)

    # Finding N-grams (words that occur together)
    from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(wordsWOStopWords)
    print("### BIGRAMS:")
    for ngram in sorted(finder.ngram_fd.items()):
        print(ngram)
    # see also nltk.TrigramAssocMeasures

    # Stemming
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    stemmedWords = [st.stem(word) for word in word_tokenize(text2)]
    print("### STEMMED WORDS:")
    print ("Original:", text2)
    print(stemmedWords)

    # Parts of Speech (Noun, Verb etc.)
    # note: requires >>> nltk.download('averaged_perceptron_tagger')
    print("### PARTS OF SPEECH:")
    for pos in nltk.pos_tag(word_tokenize(text2)):
        print(pos)
    # note: refer to nltk documentation for the meaning of pos tags (VBN, NNP etc)

    #Disambiguation
    # note: requires >>> nltk.download('wordnet')
    from nltk.corpus import wordnet as wn
    print("### DISAMBIGUATION - SYNSETS:")
    for ss in wn.synsets('wireless'):
        print(ss, ss.definition())


def disambiguate(text1, text2, term):
    from nltk.wsd import lesk
    print("### DISAMBIGUATION - LESK:")
    sense1 = lesk(word_tokenize(text1),term)
    print(sense1, sense1.definition())

    sense2 = lesk(word_tokenize(text2),term)
    print(sense2, sense2.definition())