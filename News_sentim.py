#!pip install spacytextblob
#!pip install requests_html
'''
'''
from bs4 import BeautifulSoup
import requests
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from requests_html import HTMLSession
'''
'''
search = 'inflation'
url = 'https://news.google.com/rss/search?q=' + search
titles = []
s = HTMLSession()
r = s.get(url)
for title in  r.html.find('title'):
  title = title.text
  titles.append(set(title.lower().split()))
print(titles)

#for t in titles:
#  if not want.intersection(t):
#    titles.remove(t)
#  if no_want.intersection(t):
#    titles.remove

print('new titles:\n' + str(titles))
'''
'''
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
for t in titles:
  text = str(t)
  space = nlp(text)
  if space._.blob.polarity == 0:
    titles.remove(t)
  elif space._.blob.polarity != 0:
    print(str(t) + ':\n' + str(space._.blob.polarity))
