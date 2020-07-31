from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from collections.abc import Mapping
import time
import os
import subprocess
import stat
import atexit
import random 
import logging

class ChromeDriver:

    def __init__(self):
        options = self.configDriver()
        self.driver = self.launchDriver(options)
        # atexit.register(self.goodbye)

    ### Code to Execute If Selenium Unexpectedly Exits
    
    def goodbye(self):
        ActionChains(self.driver).send_keys(Keys.ALT, 'F').send_keys('X')
    def configDriver(self):
        options = webdriver.ChromeOptions()                         
        options.add_extension("C:/Users/harri/Documents/Programming/Pure_Skills/Python/SeleniumDriver/pdf_viewer.crx")
        options.set_capability('unhandledPromptBehavior', 'accept') ## allow prompts
        return options
    def launchDriver(self, options):
        subprocess.call("bash dGCache", shell=True) ## Remove Cache      
        driver = webdriver.Chrome(options=options)
        print("Driver at launchDriver:", driver)
        return driver
    def relevantHashTag(self, searchInterest):
        """
            Title: relevantHashTag
            Description: Find All Relevant Hashtags related to a searchInterest
            returns: All Hashtags 
            params: 
                @self.driver -- The WebDriver
                @searchInterest -- User's search query on best-hashtags
        """
        ## Context
        self.driver.get("https://best-hashtags.com/")
        searchBar = self.driver.find_element_by_id("cauta")
        searchButton = self.driver.find_element_by_css_selector(".btn-u")
        
        searchBar.send_keys(searchInterest)
        searchButton.click() 
        time.sleep(5)
        firstTagBox = self.driver.find_element_by_css_selector(".tag-box:nth-child(5) *:first-child")
        secondTagBox = self.driver.find_element_by_css_selector(".tag-box:nth-child(10) *:first-child")
        print(firstTagBox.text + secondTagBox.text)
        return firstTagBox.text + secondTagBox.text
    def searchGoogle(self, tags):
        self.driver.get("https://google.com/")
        time.sleep(5)
        
        for tag in tags:
            searchBar = self.driver.find_element_by_css_selector("input[name='q']")
            searchBar.clear()
            searchBar.send_keys(tag, Keys.ENTER)
            delay = int(random.randrange(60, 120))

            ## Don't sleep if only one element is searched
            if len(tags) == 1:
                return 0

            print("Sleeping for", delay)
            time.sleep(delay)

    def searchAmazon(self, tags):
        self.driver.get("https://www.amazon.com/")
        for tag in tags:
            searchBar = self.driver.find_element_by_css_selector("input[name='field-keywords']")
            searchBar.clear()
            searchBar.send_keys(tag, Keys.ENTER)
            delay = int(random.randrange(60, 120))
            print("Sleeping for", delay)
            time.sleep(delay)
    
    ## Get All Links Present on a page
    def getLinks(self, link):
        return 0
    ## Always returns a "not None" value
    def getSelectedText(self):

        ## Selects text in browser, in pdf, or returns empty string        
        browserText = self.driver.execute_script("return window.getSelection().toString()") 
        documentText = self.driver.execute_script("return document.getSelection().toString()")
        text = browserText if (any(browserText)) else documentText
        base = self.driver.execute_script("return window.getSelection().baseNode") or \
        self.driver.execute_script("return document.getSelection().baseNode") or None

        baseText = ""
        if base == None:
            baseText = ""
        else:
            if isinstance(base, Mapping):
                parent = base["parentNode"]
                baseText = parent.text


        
        return [text, baseText] 

    def alert(self, message):
        self.driver.execute_script("alert(arguments[0])", message)
        time.sleep(2)
    def quit(self):
        self.driver.quit()
