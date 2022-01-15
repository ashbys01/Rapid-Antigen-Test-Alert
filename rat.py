#!/bin/bash
import time
import json
import requests
# selenium webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
# For Pushover
import http.client, urllib

# The RATS!
from ratart import *

#Surrounding Suburbs
from suburbs import getSuburbs

settings = json.load(open("settings.json"))

def pushme( title, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": settings['token'],
        "user": settings['user_key'],
        "message": message,
        "title": title,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def init():
    global driver
    current_time = time.localtime()
    # assign headless driver for site navigation
    options = EdgeOptions()
    options.use_chromium = True
    # options.headless = True
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument("--log-level=3")
    # create the driver with timeout management
    driver = Edge(options=options)

    locations = getSuburbs()
    locations.insert(0,"")
    wait = WebDriverWait(driver, settings['wait_timer'])
    minutes = settings['refresh_timer']
    # Lets Go
    print("Opening 'Find a RAT' and searching suburbs within "+str(settings["radius"])+"km of "+settings["suburb"])
    theRat()
    driver.get("https://findarat.com.au/")
    while True: # Keep it going
        wait.until(element_to_be_clickable((By.CSS_SELECTOR, "#__next > div > div.css-1k7hwcb > div > div.css-1y52w7m > div.css-bplzly > span:nth-child(3)"))).click()
        locs = 0
        ress = 0
        results = []
        for location in locations[1:]:
            time.sleep(4)
            wait.until(element_to_be_clickable((By.CLASS_NAME, "chakra-input"))).clear()
            wait.until(element_to_be_clickable((By.CLASS_NAME, "chakra-input"))).send_keys(location)
            print(f'Searching {location}...')
            locs+=1
            locats = driver.find_elements(By.CLASS_NAME, "css-fiqz9x")
            
            # result = driver.find_element_by_selector("css-14dtuui").text
            if (locats):
                for e in locats:
                    result = []
                    in_stock = e.text.find("In Stock")
                    age = e.text.find("minutes")
                    if (in_stock > 0 and age > 0):
                        locat = e.find_elements(By.TAG_NAME, "p")
                        locatName = e.find_element(By.TAG_NAME, "h2")
                        result.append(locatName.text)
                        result.append(locat[1].text)
                        result.append(locat[3].text)
                        
                        if(len(locat)>4):
                            result.append(locat[4].text)
                        results.append(result)
                        ress+=1
            else:
                continue
            
        print(f'Finished scurrying through {locs} suburbs.')
        if(len(results)!=0):
            ratFound()
            loc = str(f"Found a RAT at {len(results)} location(s):")
            print(time.strftime('%I:%M %p', current_time)+"  "+loc)
            # print(loc)
            rats=""
            for p in results:
                rat = "\n".join(p)
                print(*p,sep="\n")
                print("\n")
                rats += (f"{rat}\n\n")
            pushme(loc,rats)
        else:
            print("\n"+time.strftime('%I:%M %p', current_time)+"  No RAT's Found!\n")
        print(f"Going to rest for {minutes} minutes...")
        time.sleep(settings["refresh_timer"]*60)
if __name__ == '__main__':
    init()