from bs4 import BeautifulSoup
import urllib
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import re
import json
import openpyxl

def GetUserInput():
    #hood = input("Enter an NYC neighborhood: ").replace(" ", "%20")
    #date = input("Enter a date for the reservation as MM/DD: ")
    #time = input("Enter a time for the reservation as HH:TT AM/PM: ")
    #party_size = str(input("Enter a party size: "))
    hood = "murray%20hill"
    date = "03/12"
    time = "07:30 PM"
    party_size = "2"
    return hood, date, time, party_size

def PrepInputsForUrl(date, time):
    current_year = str(datetime.datetime.now().year)
    month, day = date.split("/")
    hour, minutes, am_pm = re.split("\s|\:", time)
    if am_pm == "PM":
        hour = str(int(hour) + 12)
    return current_year, month, day, hour, minutes, am_pm

def SetUpSelenium():
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    options.headless = True
    #options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver

def ScrapeOpenTable (hood, date, time, party_size):
    #Prepare date/time inputs for url
    current_year, month, day, hour, minutes, am_pm = PrepInputsForUrl(date, time)
    #url
    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers="+party_size+"&metroId=8term="+hood
    print(url)
    #set up selenium
    driver = SetUpSelenium()
    driver.get(url)
    #scroll and execute js
    javaScript = "window.scrollBy(0,1000);"
    driver.execute_script(javaScript)
    #identify all <script> elements since this is where the restaurant data is located.
    elements = driver.find_elements_by_tag_name("script")
    #<script> element with restaurant data is the -2 element in list.
    element = elements[-2].get_attribute("innerHTML")
    #substring of element containing dictionary with restaurant data
    script_data = element[element.find("\"restaurants\":")+14:element.find("\"totalRestaurantCount\":")-1]
    #convert json script data (in string format) --> dictionary (json.loads) --> dataframe (DataFrame.from_dict)
    df = pd.DataFrame.from_dict(json.loads(script_data))
    #quit driver
    driver.quit()
    return df

def getReservationTimes(df, date, time, party_size):
    #Only perform for first 3 restaurants for testing
    df1 = df.head(3)
    #Create a "times" column in the df
    df1["times"] = ""
    #Prepare date/time inputs for url
    current_year, month, day, hour, minutes, am_pm = PrepInputsForUrl(date, time)
    #set up selenium
    driver = SetUpSelenium()
    #loop through df
    for index, row in df1.iterrows():
        #Get restaurant from URL and then navigate to page with specified user inputs
        url = row["urls"]["profileLink"]["link"]
        url = url+"?p="+party_size+"&sd="+current_year+"-"+month+"-"+day+"T"+hour+"%3A"+minutes+"%3A00"
        #scrape webpage
        driver.get(url)
        #find script elements on webpage
        elements = driver.find_elements_by_tag_name("script")
        #<script> element with times is the -3 element in list.
        element = elements[-3].get_attribute("innerHTML")
        #convert substring of available times to a list
        times_list = json.loads(element[element.find("\"times\":")+8:element.find("\"noTimesMessage\":")-1])
        #list variable to store string format times for restaurant
        times_list_string = []
        #collect string format times
        for time in times_list:
            times_list_string.append(time["timeString"])
        #store string format times in df
        df1.at[index, "times"] = times_list_string
    #quit driver
    driver.quit()
    df1.to_excel("OTrestaurants.xlsx")

def main():
    hood, date, time, party_size = GetUserInput()
    df = ScrapeOpenTable(hood, date, time, party_size)
    getReservationTimes(df, date, time, party_size)

if __name__ == "__main__":
    main()
