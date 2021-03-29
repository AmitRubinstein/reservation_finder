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
import InputsUI
from requests_html import HTMLSession


#Function to convert user inputs into URL format to query the search.
def prepInputsForUrl(date, time):
    month, day, year = date.split("/")
    hour, minutes, am_pm = re.split("\s|\:", time)
    if am_pm == "PM":
        hour = str(int(hour) + 12)
    return year, month, day, hour, minutes, am_pm

#Function to configure Selenium and create a driver object.
def setUpSelenium():
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver

#Function to configure BeautifulSoup and create a soup object.
def setUpBS(url):
    #page = urllib.request.urlopen(url)
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render()
    soup = BeautifulSoup(resp.html.html, "lxml")
    return soup

#Query the search on OpenTable and return results as a DataFrame.
def scrapeOpenTable (date, time, party_size, hood):
    #generate url
    year, month, day, hour, minutes, am_pm = prepInputsForUrl(date, time)
    url = "https://www.opentable.com/s?dateTime="+year+"-"+month+"-"+day+"T"+hour+"%3"+"A"+minutes+"%3A00&covers="+str(party_size)+"&term="+hood.replace(" ", "%20")
    print(url)
    #set up selenium
    driver = setUpSelenium()
    driver.get(url)
    ##print(driver.page_source)
    #scroll and execute js
    javaScript = "window.scrollBy(0,1000);"
    driver.execute_script(javaScript)
    #identify all <script> elements - elemnt -2 is where the target data is located.
    elements = driver.find_elements_by_tag_name("script")
    element = elements[-2].get_attribute("innerHTML")
    #Pull substring of element containing dictionary with restaurant data
    script_data = element[element.find("\"restaurants\":")+14:element.find("\"totalRestaurantCount\":")-1]
    driver.quit()
    #convert json script data (in string format) --> dictionary (json.loads) --> dataframe (DataFrame.from_dict)
    #.head(3) for testing purposes
    df = pd.DataFrame.from_dict(json.loads(script_data)).head(3)
    #remove unneeded data columns and add new columns
    df = df.drop(["restaurantId", "isPromoted", "hasTakeout", "type", "campaignId", "isPinned", "photos", "justAddedDetails", "matchRelevance", "orderOnlineLink", "features", "restaurantAvailabilityToken", "__typename", "offers", "deliveryPartners"], axis=1)
    df["times"] = ""
    df["open table rating"] = None
    #df["num of open table ratings"] = None
    df["yelp rating"] = None
    df["num of ratings"] = None
    #Clean and format data
    for index, row in df.iterrows():
        df.at[index, "urls"] = row["urls"]["profileLink"]["link"]
        df.at[index, "priceBand"] = row["priceBand"]["priceBandId"]
        df.at[index, "neighborhood"] = row["neighborhood"]["name"]
        df.at[index, "primaryCuisine"] = row["primaryCuisine"]["name"]
        df.at[index, "topReview"] = row["topReview"]["highlightedText"]
        df.at[index, "open table rating"] = str(row["statistics"]["reviews"]["ratings"]["overall"]["rating"]) + " (" + str(row["statistics"]["reviews"]["allTimeTextReviewCount"]) + ")"
        #df.at[index, "num of open table ratings"] = row["statistics"]["reviews"]["allTimeTextReviewCount"]
        df.at[index, "description"] = row["description"].replace("<br />", " ")
    df = df.drop(["statistics"], axis=1)
    return df

#Loop through the individiual pages for each restaurant returned in scrapeOpenTable and scrape the available times.
def getReservationTimes(df, date, time, party_size):
    year, month, day, hour, minutes, am_pm = prepInputsForUrl(date, time)
    driver = setUpSelenium()
    for index, row in df.iterrows():
        #Get restaurant from URL and then navigate to page with specified user inputs
        url = row["urls"]
        url = url+"?p="+str(party_size)+"&sd="+year+"-"+month+"-"+day+"T"+hour+"%3A"+minutes+"%3A00"
        print(url)
        driver.get(url)
        #find script elements on webpage <script> element with times is the -3 element in list.
        elements = driver.find_elements_by_tag_name("script")
        element = elements[-3].get_attribute("innerHTML")
        #convert substring of available times to a list
        times_list = json.loads(element[element.find("\"times\":")+8:element.find("\"noTimesMessage\":")-1])
        available_times = []
        #store available times in dataframe
        for time in times_list:
            available_times.append(time["dateTime"])
        #store string format times in df
        df.at[index, "times"] = available_times
    driver.quit()
    return df

#Utilize BeautifulSoup to scrape yelp ratings from bing search
def getYelpReviews(df):
    for index, row in df.iterrows():
        url = "https://www.bing.com/search?q="+row["name"].replace(" ","+")+row["contactInformation"]["phoneNumber"]+"+yelp+restaurant"
        print(url)
        soup = setUpBS(url)
        yelp_rating = soup.find("div", class_="b_sritem b_srtxtstarcolor").get_text()
        num_of_ratings = yelp_rating[yelp_rating.find("(")+1:-1]
        yelp_rating = yelp_rating[:yelp_rating.find("/")]
        df.at[index, "yelp rating"] = float(yelp_rating)
        df.at[index, "num of ratings"] = num_of_ratings
    df_filtered = df[df["yelp rating"] >= 4]
    return df_filtered

#Orchestrate execution of script and return the generated dataframe as a spreadsheet.
def main():
    date, time, party_size, hood = InputsUI.getUserInput()
    df = scrapeOpenTable(date, time, party_size, hood)
    df = getYelpReviews(df)
    df = getReservationTimes(df, date, time, party_size)
    df.to_csv("OTrestaurants.csv")
    df = pd.read_csv("OTrestaurants.csv")
    InputsUI.showSearchResults(df, date, time, party_size, hood)

if __name__ == "__main__":
    main()
