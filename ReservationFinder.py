from bs4 import BeautifulSoup
import urllib.request
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import re
import json
import openpyxl

def getUserInput():
    #hood = input("Enter an NYC neighborhood: ").replace(" ", "%20")
    #date = input("Enter a date for the reservation as MM/DD: ")
    #time = input("Enter a time for the reservation as HH:TT AM/PM: ")
    #party_size = str(input("Enter a party size: "))
    hood = "murray%20hill"
    date = "03/12"
    time = "07:30 PM"
    party_size = "2"
    return hood, date, time, party_size

def prepInputsForUrl(date, time):
    current_year = str(datetime.datetime.now().year)
    month, day = date.split("/")
    hour, minutes, am_pm = re.split("\s|\:", time)
    if am_pm == "PM":
        hour = str(int(hour) + 12)
    return current_year, month, day, hour, minutes, am_pm

def setUpSelenium():
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver

def setUpBS(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    return soup

def scrapeOpenTable (hood, date, time, party_size):
    #Prepare date/time inputs for url
    current_year, month, day, hour, minutes, am_pm = prepInputsForUrl(date, time)
    #generate url
    url = "https://www.opentable.com/s?dateTime="+current_year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers="+party_size+"&term="+hood
    print(url)
    #set up selenium
    driver = setUpSelenium()
    driver.get(url)
    ##print(driver.page_source)
    #scroll and execute js
    javaScript = "window.scrollBy(0,1000);"
    driver.execute_script(javaScript)
    #identify all <script> elements - this is where the target data is located.
    elements = driver.find_elements_by_tag_name("script")
    #<script> element with restaurant data is the -2 element in list.
    element = elements[-2].get_attribute("innerHTML")
    #substring of element containing dictionary with restaurant data
    script_data = element[element.find("\"restaurants\":")+14:element.find("\"totalRestaurantCount\":")-1]
    #quit driver
    driver.quit()
    #convert json script data (in string format) --> dictionary (json.loads) --> dataframe (DataFrame.from_dict)
    #.head(3) for testing purposes
    df = pd.DataFrame.from_dict(json.loads(script_data)).head(3)
    #remove unneeded data columns
    df = df.drop(["type", "campaignId", "isPinned", "photos", "justAddedDetails", "matchRelevance", "orderOnlineLink"], axis=1)
    #Create "times" and "yelp rating" columns in the df
    df["times"] = ""
    df["yelp rating"] = ""
    #Clean data
    for index, row in df.iterrows():
        df.at[index, "urls"] = row["urls"]["profileLink"]["link"]
        df.at[index, "priceBand"] = row["priceBand"]["priceBandId"]
        df.at[index, "neighborhood"] = row["neighborhood"]["name"]
        df.at[index, "primaryCuisine"] = row["primaryCuisine"]["name"]
        #df.at[index, "topReview"] = row["topReview"]["highlightedText"]
    return df

def getReservationTimes(df, date, time, party_size):
    #Prepare date/time inputs for url
    current_year, month, day, hour, minutes, am_pm = prepInputsForUrl(date, time)
    #set up selenium
    driver = setUpSelenium()
    #loop through df
    for index, row in df.iterrows():
        #Get restaurant from URL and then navigate to page with specified user inputs
        url = row["urls"]
        url = url+"?p="+party_size+"&sd="+current_year+"-"+month+"-"+day+"T"+hour+"%3A"+minutes+"%3A00"
        #scrape webpage
        driver.get(url)
        #find script elements on webpage
        elements = driver.find_elements_by_tag_name("script")
        #<script> element with times is the -3 element in list.
        element = elements[-3].get_attribute("innerHTML")
        #convert substring of available times to a list
        times_list = json.loads(element[element.find("\"times\":")+8:element.find("\"noTimesMessage\":")-1])
        #list variable to store desired time data
        available_times = []
        #collect available times
        for time in times_list:
            available_times.append(time["dateTime"])
        #store string format times in df
        df.at[index, "times"] = available_times
    #quit driver
    driver.quit()
    return df

#Utilize BeautifulSoup to scrape yelp ratings from bing search
def getYelpReviews(df):
    for index, row in df.iterrows():
        url = "https://www.bing.com/search?q="+row["name"].replace(" ","+")+row["contactInformation"]["phoneNumber"]+"+yelp+restaurant"
        soup = setUpBS(url)
        yelp_rating = soup.find("div", class_="b_sritem b_srtxtstarcolor").get_text()
        df.at[index, "yelp rating"] = yelp_rating
    return df

def main():
    hood, date, time, party_size = getUserInput()
    df = scrapeOpenTable(hood, date, time, party_size)
    df = getReservationTimes(df, date, time, party_size)
    df = getYelpReviews(df)
    df.to_excel("OTrestaurants.xlsx")


if __name__ == "__main__":
    main()
