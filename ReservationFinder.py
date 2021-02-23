from bs4 import BeautifulSoup
import urllib
import datetime
import pandas as pd
import requests
import re

def GetUserInput():
    #hood = input("Enter an NYC neighborhood: ").replace(" ", "%20")
    #date = input("Enter a date for the reservation as MM/DD: ")
    #time = input("Enter a time for the reservation as HH:TT AM/PM: ")
    hood = "murray%20hill"
    date = "07/26"
    time = "07:30 PM"
    return hood, date, time

def ScrapeOpenTable (hood, date, time):
    #Prepare inputs for url
    current_year = str(datetime.datetime.now().year)
    month, day = date.split("/")
    hour, minutes, am_pm = re.split("\s|\:", time)
    if am_pm == "PM":
        hour = str(int(hour) + 12)
    #prep the soup
    #with requests.Session() as s:
    #    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers=2&metroId=8term="+hood
    #    print(url)
    #    r = s.get(url, headers=req_headers)
    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers=2&metroId=8term="+hood
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
    restuarant_listings = soup.find_all("div", {"data-test":"restaurant-cards"})
    print(restuarant_listings)


def main():
    hood, date, time = GetUserInput()
    ScrapeOpenTable(hood, date, time)

if __name__ == "__main__":
    main()
