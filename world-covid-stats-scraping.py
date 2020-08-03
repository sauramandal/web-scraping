import requests, datetime
from bs4 import BeautifulSoup
import pandas as pd


def scrapeGlobalCase():
    try:
        url = "https://www.worldometers.info/coronavirus/"
        req = requests.get(url)
        bsObj = BeautifulSoup(req.text, "html.parser")
        data = bsObj.find_all("div", class_="maincounter-number")
        numConfirmed = int(data[0].text.strip().replace(',', ''))
        numDeaths = int(data[1].text.strip().replace(',', ''))
        numRecovered = int(data[2].text.strip().replace(',', ''))
        numActive = numConfirmed - numDeaths - numRecovered
        timeNow = datetime.datetime.now()
        return {
            'Date': str(timeNow),
            'ConfirmedCases': numConfirmed,
            'ActiveCases': numActive,
            'RecoveredCases': numRecovered,
            'Deaths': numDeaths
        }
    except Exception as e:
        print(e)


results = scrapeGlobalCase()
#df = pd.DataFrame()
print(results)
