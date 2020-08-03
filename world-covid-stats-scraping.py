from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import datetime
from bs4 import BeautifulSoup

# Scrape World Covid Stats


def scrapeGlobalCase(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
        data = bs.find_all("div", class_="maincounter-number")
        numConfirmed = int(data[0].text.strip().replace(',', ''))
        numDeaths = int(data[1].text.strip().replace(',', ''))
        numRecovered = int(data[2].text.strip().replace(',', ''))
        numActive = numConfirmed - numDeaths - numRecovered
        timeNow = datetime.datetime.now()
        return {
            'date': str(timeNow),
            'ConfirmedCases': numConfirmed,
            'ActiveCases': numActive,
            'RecoveredCases': numRecovered,
            'Deaths': numDeaths
        }
    except Exception as e:
        print(e)


results = scrapeGlobalCase("https://www.worldometers.info/coronavirus/")
print(results)
