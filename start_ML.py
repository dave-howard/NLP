from nltk_test.get_web_data import get_articles, get_article_text

url = "http://doxydonkey.blogspot.com/"

links = []
get_articles(url, links)

for url in links:
    get_article_text(url)