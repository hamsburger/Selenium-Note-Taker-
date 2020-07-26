from pynput import keyboard
from pynput.keyboard import Key, Controller 
import time
import re
import atexit
import logging 
import sys

## Update urlKnowledge, url, currBaseText in Real Time (Setter)
## Update Level on Keypress  
# class keyThread:

class KeyThread:
    '''
    '''
    def __init__(self, driver):
        self.level = 0
        self.driver = driver
        self.urlKnowledge = ""
        self.url = ""
        self.currBaseText = "" 
        print("Init!")


    def updateMainThread(self):
        return {"urlKnowledge" : self.urlKnowledge, "url" : self.url, "currBaseText" : self.currBaseText, "level" : self.level}

    ## This only needs to be updated upon adding text (highlighting text) 
    def updateKeyThread(self, url, urlKnowledge, currBaseText):
        self.url = url
        self.urlKnowledge = urlKnowledge
        self.currBaseText = currBaseText 
    
    def traverseTillSpace(self, start, end, currBaseText, recentKnowledge):
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

    def activateHotKeys(self):  
        def addLevel():
            self.level += 1
            print("Added level: ", self.level)
            

        def subtractLevel():
            if self.level > 0:
                self.level -= 1
            print("Subtract Level: ", self.level)
            

        def fillText():
            
            if len(self.urlKnowledge[self.url]) == 0:
                return 

            recentKnowledge = self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"]
            searchF = re.search(recentKnowledge, self.currBaseText, re.I)
            if searchF == None:
                return 

            start = searchF.start()
            end = searchF.end()
            newStart, newEnd = self.traverseTillSpace(start, end, self.currBaseText, recentKnowledge)
            self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"] = self.currBaseText[newStart:newEnd]
            print("Text formatted from: " + recentKnowledge + " to " + self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"])
            

        def pop():
            if len(self.urlKnowledge[self.url]) != 0:
                poppedString = "Pop " + self.urlKnowledge[self.url].pop()["detail"]

                if len(self.urlKnowledge[self.url]) != 0:
                    self.currBaseText = self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"]
                print(poppedString)
                return

            print("Can't Pop. No Knowledge In The List")
            
        def printKnowledge():
            print(self.urlKnowledge[self.url])
    
        ## Keys Are Ready
        hotKeys = keyboard.GlobalHotKeys({
            '<shift>+-' : subtractLevel,
            '<shift>+=' : addLevel,
            '<shift>+f' : fillText, 
            '<shift>+p' : printKnowledge,
            '<esc>' : pop,
        })
        
        hotKeys.start()
        return hotKeys

if __name__ == "__main__":
    activateHotKeys()