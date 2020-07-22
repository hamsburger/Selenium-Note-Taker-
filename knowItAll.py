"""
    Title: knowItAll.py
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
from collections import defaultdict
sys.path.append("..")
import ChromeDriver
import keyHandler

def traverseTillSpace(start, end, currBaseText, recentKnowledge):
    '''
        From the first match, traverse till first space or till beginning. 
    '''
    
    newStart = start
    newEnd = end

    while currBaseText[newEnd] != " " and newEnd < len(currBaseText) - 1:
        newEnd += 1
    
    while currBaseText[newStart] != " " and newStart > 0:
        newStart -= 1            
    
    return [newStart, newEnd]

def logException():
    logging.exception("-------------------------------------------------------\nException Occured")

def isAddTextValid(prevText, text, learnedDetails):
    '''
        Title: isAddTextValid
        Context: @prevText -- text found 0.5 seconds before @text is found.
                 @learnedDetails -- List of knowledge that are already selected.

        Description: Finds prevText at 0-0.5 seconds, and finds text in 0.5s-1s. 
                     If text === prevText, text is added to learnedDetails. If not, text is not added
                     This ensures that text is only added to learnedDetails when the same amount
                     of text is highlighted for a certain duration.       
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
    print(focus, learnedDetails)
    fileName = focus + "--" + str(datetime.date.today())
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
    learnedDetails = []
    prevText = ""
    currBaseText = ""
    level = 0
    urlKnowledge = defaultdict(list) # key -> url, value -> list of highlighted text
    focus = input("What is Your Focus?")

    
    while True:
        try: 
            url = driver.driver.current_url
            time.sleep(0.5) ## Time it takes to find first instance of text: 0s - 0.5s 
            text, baseText = driver.getSelectedText()
            text = re.sub("[\\t\\n]+", " ", text).strip() ## Remove line breaks and tabs, and also any punctuation at the end. 
            text = re.sub("[\.\?\,]$", "", text)
            text = text[0:1].upper() + text[1:]
            

            if isAddTextValid(prevText, text, urlKnowledge[url]):
                urlKnowledge[url].append({"detail" : text, "level" : level})
                currBaseText = baseText 

            handleOperation(driver, urlKnowledge, url, currBaseText)
            level = handleTabLevel(driver, level)            
            print(str(level) + ". ")
            for knowledge in urlKnowledge[url]:
                print(knowledge["detail"] + "\n")
                
            prevText = text
        except KeyboardInterrupt:
            WriteOutlearnedDetails(focus, urlKnowledge)
            sys.exit(0)

if __name__ == "__main__":
    main()

## After every chrome process, use Alt+F and X to Shut it Down For School 
                            
