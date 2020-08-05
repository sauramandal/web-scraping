from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

pages = set()
allExtLinks = set()
allIntLinks = set()

# Get named headlines from BBC News


def getBBCHeadlines(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
        images_container = bs.find_all(
            'div', {'class': "gs-o-responsive-image"})
        images = bs.find_all('img', {'src': re.compile(
            '[-\w]+\.(?:jpg|gif|png)')}, {"class": "qa-lazyload-image"})

        #       for i in images_container:
        #             for child in i.children:
        #         print(child)
        headlines = bs.find_all('h3', {"class": "gs-c-promo-heading__title"})
    except AttributeError as e:
        return None
    return list(map(lambda headline: headline.get_text(), headlines))

# Get latest world news


def getBBCBusinessNews(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
        posts = bs.find_all('div', {"class": "gel-layout__item"})
        images_container = bs.find_all(
            'div', {'class': "gs-o-responsive-image"})
    except AttributeError as e:
        return None
    return posts

# Recursively crawling an entire site
# Wiki crawler


def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)

# Retrieves a list of all Internal links found on a page


def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,
                                  urlparse(includeUrl).netloc)
    internalLinks = []
    # Finds all links that begin with a "/"
    for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

# Retrieves a list of all external links found on a page


def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    # Finds all links that start with "http" that do
    # not contain the current URL
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    domain = '{}://{}'.format(urlparse(siteUrl).scheme,
                              urlparse(siteUrl).netloc)
    bs = BeautifulSoup(html, 'html.parser')
    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)


bbc_headlines = getBBCHeadlines("https://www.bbc.com/news/business")
bbc_latest_news = getBBCHeadlines("https://www.bbc.com/news/world")
if bbc_headlines == None:
    print("Headlines could not be found")
else:
    print(bbc_headlines)
allIntLinks.add('http://oreilly.com')
getAllExternalLinks('http://oreilly.com')
getLinks('')
