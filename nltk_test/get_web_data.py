
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


# get article text from IT blog http://doxydonkey.blogspot.com/
def get_articles(url, links, n):
    print("GETTING (",n,")", url)
    response = urlopen(url).read()
    soup = BeautifulSoup(response, "lxml")
    print("PROCESSING...")
    for a in soup.find_all('a'):
        try:
            url = a['href']
            title = a['title']
            #print(title, url)
            if title == "Older Posts":
                print(title, url)
                if len(links) < n:
                    links.append(url)
                    get_articles(url, links, n-1)
        except:
            title = ""

# get text from <li> inside <div> with class "post-body"
def get_article_text(url):
    text = []
    print("GETTING", url)
    response = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(response, "lxml")
    print("READING...")
    my_divs = soup.find_all("div", {"class":"post-body"})
    for div in my_divs:
        print(div['class'])
        for li in div.find_all("li"):
            item = li.text #.encode("ascii", errors="replace")
            print("ITEM", item)
            text.append(item)
    return text