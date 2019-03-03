from nltk_test.nltk_basics import disambiguate, run_tests, stem_words, remove_stop_words, find_ngrams
from nltk_test.nltk_basics import auto_summarise
from nltk_test.get_web_data import get_data

text1 = "The solution will include LAN, WAN and Firewall. The LAN will include both fixed and wireless"
text2 = """The traffic will be routed by the L3 device. 
Routes will be advertised by BGP or other dynamic protocol.
Other dynamic protocols might include EIGRP or OSPF.
There will be no static routing, dynamic routing will be preferred.
The firewall will interface with the LAN switch, and will not be directly connected to the WAN router"""

#run_tests(text2)

#disambiguate(text1="the correct routing protocol will be used by the LAN switch",
#             text2="ththe standard governance protocol will be used to introduce the service",
#             term="protocol")

url = "https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/data_sheet-c78-738977.html"
url = "https://en.wikipedia.org/wiki/Leeds_United_F.C."
text = get_data(url)

for s in auto_summarise(text, 5):
    print(s)
exit(0)

words = stem_words(remove_stop_words(text))

from nltk.probability import FreqDist
freq = FreqDist(words)
print(type(freq), freq.most_common(10))
print(freq['cisco'])
print(freq.get('cisco'))

# alternative to freq.most_common()
from heapq import nlargest
common = nlargest(10, freq, key=freq.get)
print(type(common), common)

#calculating sentence significance
from collections import defaultdict
ranking = defaultdict(int)

from nltk import sent_tokenize, word_tokenize
sents = sent_tokenize(text)
print (type(sents), sents)

for i, sent in enumerate(sents):
    for w in word_tokenize(sent.lower()):
        if w in freq:
            ranking[i]+=freq[w]

# print the top 10 ranked sentences in original order
for i in sorted(nlargest(10, ranking, key=ranking.get)):
    print(i, ranking[i], sents[i])

