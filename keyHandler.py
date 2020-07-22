from pynput import keyboard
from pynput.keyboard import Key, Controller 
import time
import re

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
            print(recentKnowledge, self.currBaseText)
            if searchF == None:
                return 

            start = searchF.start()
            end = searchF.end()
            newStart, newEnd = traverseTillSpace(start, end, self.currBaseText, recentKnowledge)
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
            

        def stop():
            h.stop()
    
        ## Keys Are Ready
        hotKeys = keyboard.GlobalHotKeys({
            '<shift>+-' : subtractLevel,
            '<shift>+=' : addLevel,
            '<shift>+f' : fillText, 
            '<esc>' : pop,
            '<ctrl>+c': stop, 
        })
        
        hotKeys.start()
        return hotKeys

if __name__ == "__main__":
    activateHotKeys()