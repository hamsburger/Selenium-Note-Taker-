"""
    Title: knowItAll.pyT
    Author: Harris Zheng
    Description: Save Words Selected By User On The Web
"""
import logging
import sys
import signal
import time
import datetime
import atexit
import re
import keyboard
import threading
from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException, WebDriverException, \
NoSuchWindowException, ElementNotInteractableException, JavascriptException

import keyHandler
import variables
import ChromeDriver

def logException():
    '''
        Log Exceptions
    '''
    logging.exception("-------------------------------------------------------\nException Occured")

def processText(text : str):
    '''
        Process Text
        @param text: Process highlighted text. 
    '''
    text = re.sub("[\\t\\n]+", " ", text).strip() ## Remove line breaks and tabs, and also any punctuation at the end. 
    text = re.sub("[\.\?\,]$", "", text)
    text = text[0:1].upper() + text[1:]
    return text 

def isAddTextValid(prevText, text, learnedDetails):

    '''
        Title: isAddTextValid
        Context: @prevText -- text found 0.5 seconds before @text is found.
                 @learnedDetails -- List of knowledge that are already selected.

        Description: Finds prevText at 0-0.5 seconds, and finds text in 0.5s-1s. 
                     If text === prevText, text is added to learnedDetails. If not, text is not added
                     This ensures that text is only added to learnedDetails when it has been highlighted for a certain duration.       
    '''
    sameText = (prevText == text)
    notEmpty = (text != '')
    textAlreadyExists = False
    for item in learnedDetails:
        if item["detail"] == text:
            textAlreadyExists = True
            break  

    return sameText and notEmpty and not textAlreadyExists  
      
def WriteOutlearnedDetails(focus, learnedDetails):
    '''
        Write out knowledge in a text file.
        @param focus -- Title of text file. 
        @param learnedDetails -- Details learned, which are categorized in URLs. 
    '''
    print(focus, learnedDetails)
    fileName = focus + "--" + str(datetime.date.today()) + ".txt"
    currTime = datetime.datetime.now().time() 
    strCurrentTime = currTime.strftime("%H:%M")

    with open(fileName, "a+", encoding="utf-8") as f:
        
        ## For each url, write down its list of knowledge
        for url,knowledge in learnedDetails.items():
            if len(knowledge) != 0:
                f.write("---------------------" + strCurrentTime + " " + url + " ------------------------------------------------\n")
                for item in knowledge:
                    if (item["level"] != 0):
                        if item["level"] % 2 != 0:
                            f.write("\t" * item["level"] + "- ")
                        else:
                            f.write("\t" * item["level"] + "• ")
                    f.write(item["detail"] + "\n")
                f.write("\n")
        
def main():
    driver = ChromeDriver.ChromeDriver()
    LOG_FILENAME = "events.log"
    logging.basicConfig(filename=LOG_FILENAME, format="%(asctime)s", level=logging.ERROR, filemode='a')
    
    ## Test Website 
    prevText = ""
    currBaseText = ""
    level = 0
    fileKnowledge = defaultdict(list) # key -> fileName, value -> list of urlKnowledge 
    urlKnowledge = defaultdict(list) # key -> url, value -> list of highlighted text
    urlWindowNames = {}
    newWindowIndex = 0
    windowIndex = 0
    freeze = False

    focus = input("What is Your Focus?")
    
    keyThread = keyHandler.KeyThread(driver) 
    hotKeyThread = keyThread.activateHotKeys() ## You Must Return this thread to run multithreading?
    print(hotKeyThread)
    print("Thread Count: ", threading.active_count())
    
    while True:
        try: 
            url = driver.driver.current_url

            ## freeze loop
            while freeze:
                freeze = freeze
            
            time.sleep(0.5) ## Time it takes to find first instance of text: 0s - 0.5s 
            driver.switch_to_new_tab(newWindowIndex-1) 
            
            text, baseText = driver.getSelectedText()
            text = processText(text)         
            keyThread.updateKeyThread(url, urlKnowledge, currBaseText, len(driver.driver.window_handles)) ## Make sure key is updated without empty url values
            
            ## Add Text if Valid
            if isAddTextValid(prevText, text, urlKnowledge[url]):
                urlKnowledge[url].append({"detail" : text, "level" : level})
                currBaseText = baseText
                keyThread.updateKeyThread(url, urlKnowledge, currBaseText, len(driver.driver.window_handles))

            ## Sync keyThread values with Main Thread Values
            keyVariables = keyThread.updateMainThread()
            currBaseText, url, urlKnowledge, level, newWindowIndex, freeze = [keyVariables["currBaseText"], keyVariables["url"], \
            keyVariables["urlKnowledge"], keyVariables["level"], keyVariables["windowIndex"], keyVariables["freeze"]]
            
            # print(str(level) + ". ")
            # for knowledge in urlKnowledge[url]:
            #     print(knowledge["detail"] + "\n")
                
            prevText = text
        except NoSuchWindowException:
            driver.switch_to_new_tab(len(driver.driver.window_handles))
        except (KeyboardInterrupt, WebDriverException):
            WriteOutlearnedDetails(focus, urlKnowledge)
            logException()
            hotKeyThread.stop()
            sys.exit(0)
        

if __name__ == "__main__":
    main()

## After every chrome process, use Alt+F and X to Shut it Down For School 
                            
