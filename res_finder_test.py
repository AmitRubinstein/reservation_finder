import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import re
import json

#inputs
hood = "murray%20hill"
date = "03/12"
time = "07:30 PM"
#Prepare inputs for url
current_year = str(datetime.datetime.now().year)
month, day = date.split("/")
hour, minutes, am_pm = re.split("\s|\:", time)
if am_pm == "PM":
    hour = str(int(hour) + 12)
#url
url = "https://www.opentable.com/r/tacovision-new-york?corrid=f901422d-4bfe-4f17-abc2-f4a7333ea217&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2021-03-06T19%3A30%3A00"
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
#driver.execute_script(javaScript)
#print(driver.page_source)
elements = driver.find_elements_by_tag_name("script")
#<script> element with restaurant data is the -3 element in list.
element = elements[-3].get_attribute("innerHTML")
#substring of element containing dictionary with restaurant data
times_list = json.loads(element[element.find("\"times\":")+8:element.find("\"noTimesMessage\":")-1])
for time in times_list:
    print(time["timeString"])
#quit driver
driver.quit()
