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
    #print(driver.page_source)
    elements = driver.find_elements_by_tag_name("script")
    for i, element in enumerate(elements):
        contents = element.get_attribute("innerHTML")
        print("Element index is :" + str(i))
        print(contents)
    #element = driver.find_elements_by_tag_name("script")[9].get_attribute("innerHTML")
    #print(element)
    #quit driver
    driver.quit()

def main():
    hood, date, time = GetUserInput()
    ScrapeOpenTable(hood, date, time)

if __name__ == "__main__":
    main()
