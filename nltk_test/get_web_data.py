
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_data(url):
    print("### GETTING DATA...")
    page = urlopen(url).read().decode("utf8")
    print("### PROCESSING ...")
    soup = BeautifulSoup(page,"lxml")
    paras = map(lambda p: p.text, soup.find_all("p"))
    #for para in paras:
    #    print (para)
    text = " ".join(paras)
    #print(text)
    return text
