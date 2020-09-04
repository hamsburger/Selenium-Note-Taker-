from selenium import webdriver 
from selenium.common import exceptions as SExceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from collections.abc import Mapping
from collections import defaultdict
import sys
import time
import os
import subprocess
import stat
import atexit
import random 
import logging
import re

class ChromeDriver:

    def __init__(self):
        options = self.configDriver()
        self.windowIndex = 0
        self.driver = self.launchDriver(options)
        self.oldURL = self.driver.execute_script("return window.location.href")
        self.oldTabs = []
        # atexit.register(self.goodbye)
        

    def switch_to_new_tab(self, index=-1) -> None: 
        ''' 
            Switch driver to currently selected window_name. 
        '''
        if self.driver.window_handles[self.windowIndex] == self.driver.window_handles[index]:
            return
        
        # print("New Tab: %d" % index)
        self.driver.switch_to.window(self.driver.window_handles[index])
        self.windowIndex = index
    
    def goodbye(self):
        ActionChains(self.driver).send_keys(Keys.ALT, 'F').send_keys('X')
    def configDriver(self):
        options = webdriver.ChromeOptions()                         
        # options.add_argument("--user-data-dir=C:/Users/harri/AppData/Local/Google/Chrome/User Data")
        # options.add_argument("--profile-directory=Profile 1")
        options.add_extension("C:/Users/harri/Documents/Programming/Pure_Skills/Python/SeleniumDriver/pdf_viewer.crx")
        options.set_capability('unhandledPromptBehavior', 'accept')
        # options.add_argument("--disable-notifications")
        return options
    def launchDriver(self, options):
        # subprocess.call("bash dGCache", shell=True) ## Remove Cache      
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(4)
        print("Driver at launchDriver:", driver)
        return driver
    def maxWindow(self):
        self.driver.maximize_window()
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
        '''
            Queries Amazon on delay. 
        '''
        self.driver.get("https://www.amazon.com/")
        for tag in tags:
            searchBar = self.driver.find_element_by_css_selector("input[name='field-keywords']")
            searchBar.clear()
            searchBar.send_keys(tag, Keys.ENTER)
            delay = int(random.randrange(60, 120))
            print("Sleeping for", delay)
            time.sleep(delay)
    def loginIndeed(self, email : str, password : int):
        self.driver.get("https://ca.indeed.com/m/")
        self.maxWindow()
        
        ## Login so that we don't get annoying message
        self.driver.find_element_by_css_selector(".gnav-LoggedOutAccountLink-text").click()
        emailInput = self.driver.find_element_by_id("login-email-input")
        time.sleep(0.5)
        emailInput.send_keys(email)
        passwordInput = self.driver.find_element_by_id("login-password-input")
        time.sleep(0.5)
        passwordInput.send_keys(password)
        self.driver.find_element_by_id("login-submit-button").click()
    def indeedGetJobs(self):
        resultText = ""
        Run= True
        ## click on title and scrape text, until all titles have been exhausted
        
        while Run:
            try:
                titles = self.driver.find_elements_by_css_selector(".jobsearch-SerpJobCard")
                for title in titles:
                    time.sleep(0.5)
                    title.click()
                    vjsText = self.driver.find_element_by_id("vjs-content").text
                    # divide string into sentences and only capture sentences that contain
                    # the word experience into the word count.
                    for entry in re.split("[\.\:\n;]{1}", vjsText):
                        if "experience" in entry:
                            resultText += entry.replace("experience", "") 
                            logging.info(entry.replace("experience", ""))

                Run = False
            except (KeyError, SExceptions.NoSuchElementException) as e:
                logging.exception(e)
                self.driver.execute_script("alert('Error Occured')")
                time.sleep(2)
            except SExceptions.ElementClickInterceptedException as e:
                logging.exception(e)
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                Run= True ## disable popup --> repeat operation
            
        return resultText.strip()
        ## then go to next page
        
    ## Get All Links Present on a page
    def getLinks(self, link):
        return 0
    ## Always returns a "not None" value
    def getSelectedText(self):
        base = None
        

        ## Selects text in browser, in pdf, or returns empty string        
        browserText = self.driver.execute_script("return window.getSelection().toString()") 
        documentText = self.driver.execute_script("return document.getSelection().toString()")
        text = browserText if (any(browserText)) else documentText

        
        try : 
            base = self.driver.execute_script("return window.getSelection().baseNode") or \
            self.driver.execute_script("return document.getSelection().baseNode") or None
        except selenium.common.exceptions.JavascriptException:
            print("BaseNode Error") ## Nullify Circular Reference Error. 
            
        
        # A piece of text may not always have a parent. 
        baseText = "" if base == None else base["parentNode"].text if isinstance(base, Mapping) else ""
        # if base == None:
        #     baseText = ""
        # else:
        #     # Only accept base text when it is a Mapping Type (For example, a dictionary)
        #     if isinstance(base, Mapping):
        #         parent = base["parentNode"]
        #         baseText = parent.text

        return [text, baseText] 
    
    def getCurrURL(self):
        return self.driver.current_url

    def alert(self, message):
        self.driver.execute_script("alert(arguments[0])", message)
        time.sleep(2)
    def quit(self):
        self.driver.quit()
