from bs4 import BeautifulSoup
import urllib
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import re

def GetUserInput():
    #hood = input("Enter an NYC neighborhood: ").replace(" ", "%20")
    #date = input("Enter a date for the reservation as MM/DD: ")
    #time = input("Enter a time for the reservation as HH:TT AM/PM: ")
    hood = "murray%20hill"
    date = "03/06"
    time = "07:30 PM"
    return hood, date, time

def ScrapeOpenTable (hood, date, time):
    #Prepare inputs for url
    current_year = str(datetime.datetime.now().year)
    month, day = date.split("/")
    hour, minutes, am_pm = re.split("\s|\:", time)
    if am_pm == "PM":
        hour = str(int(hour) + 12)
    #url
    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers=2&metroId=8term="+hood
    print(url)
    #set up selenium
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    #options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(url)
    #scroll and execute js
    javaScript = "window.scrollBy(0,1000);"
    driver.execute_script(javaScript)
    #print contents
    print(driver.page_source)
    driver.find_elements
    #quit driver
    driver.quit()

    #prep the soup
    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers=2&metroId=8term="+hood
    print(url)
    #html = urllib.request.urlopen(url).read()
    #soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
    #print(soup)
    #restuarant_listings = soup.find("div", {"data-test":"restaurant-cards"})
    #print(restuarant_listings)
    #rest_names = soup.find_all("a", {"data-test":"res-card-name"})
    #for name in rest_names:
    #    print(name.text)
    #for listing in restuarant_listings:
    #    print(listing)
    #    name = listing.get("h6")
        #name = listing.find("a", {"data-test":"res-card-name"})
    #    print(name)


def main():
    hood, date, time = GetUserInput()
    ScrapeOpenTable(hood, date, time)

if __name__ == "__main__":
    main()
