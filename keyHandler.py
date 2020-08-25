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
        self.windowIndex = 0
        self.numWindows = 0
        self.freeze = False
        print("Init!")


    def updateMainThread(self):
        return {"urlKnowledge" : self.urlKnowledge, "url" : self.url, "currBaseText" : self.currBaseText, "level" : self.level, "windowIndex" : self.windowIndex,
        "freeze" : self.freeze}

    ## This only needs to be updated upon adding text (highlighting text) 
    def updateKeyThread(self, url, urlKnowledge, currBaseText, numWindows):
        self.url = url
        self.urlKnowledge = urlKnowledge
        self.currBaseText = currBaseText 
        self.numWindows = numWindows

    def traverseTillSpace(self, start, end, currBaseText, recentKnowledge):
        '''
            From the first match, traverse till first space or till beginning. 
        '''
    
        newStart = start
        newEnd = end

        while newEnd < len(currBaseText) and currBaseText[newEnd] != " ":
            newEnd += 1
        
        while newStart > 0 and currBaseText[newStart] != " ":
            newStart -= 1        
        
        return [newStart, newEnd]

    def isFreeze(self):
        return self.freeze

    def activateHotKeys(self):  
        def addLevel():
            if self.isFreeze(): return
            self.level += 1
            print("Added level: ", self.level)
            
        def subtractLevel():
            if self.isFreeze(): return
            if self.level > 0:
                self.level -= 1
            print("Subtract Level: ", self.level)
            
        def fillText():
            if self.isFreeze(): return
            if len(self.urlKnowledge[self.url]) == 0:
                return 

            recentKnowledge = self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"]
            print(recentKnowledge, self.currBaseText)
            searchF = re.search(recentKnowledge, self.currBaseText, re.I)
            if searchF == None:
                return 

            start = searchF.start()
            end = searchF.end()
            newStart, newEnd = self.traverseTillSpace(start, end, self.currBaseText, recentKnowledge)
            self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"] = self.currBaseText[newStart:newEnd]
            print("Text formatted from: " + recentKnowledge + " to " + self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"])
            
        def pop():
            if self.isFreeze(): return
            if len(self.urlKnowledge[self.url]) != 0:
                poppedString = "Pop " + self.urlKnowledge[self.url].pop()["detail"]

                if len(self.urlKnowledge[self.url]) != 0:
                    self.currBaseText = self.urlKnowledge[self.url][len(self.urlKnowledge[self.url]) - 1]["detail"]
                print(poppedString)
                return

            print("Can't Pop. No Knowledge In The List")

        def freeze():
            self.freeze = not self.freeze
            print("Freeze: %r" % (self.freeze))
            
        def printKnowledge():
            if self.isFreeze(): return
            print(self.urlKnowledge[self.url])

        def changeWindowHandle():
            if self.isFreeze(): return
            inputValid = False
            windowIndex = ""
        
            while not inputValid:
                try: 
                    windowIndex = input("Which window index would you like to switch to?")
                    match = re.match(r"^[0-9]+$", windowIndex)
                    
                    ## Check integer >= 0
                    if match == None:
                        print("Please enter an integer >= 0.")
                        continue

                    windowIndex = int(windowIndex)

                    ## check selected index less than number of windows  
                    if windowIndex >= self.numWindows:
                        print("Index >= length of window handles.")
                        continue

                    inputValid = True
                except:
                    inputValid = False 
            
            print("Switched to Index", str(windowIndex))
            self.windowIndex = windowIndex

        ## Keys Are Ready
        hotKeys = keyboard.GlobalHotKeys({
            '<shift>+-' : subtractLevel,
            '<shift>+=' : addLevel,
            '<shift>+f' : fillText, 
            '<shift>+p' : printKnowledge,
            '<alt>+<shift>+f' : freeze,
            '<alt>+s' : changeWindowHandle,
            '<esc>' : pop,
        })
        
        hotKeys.start()
        return hotKeys


def getFalse():
    return False
if __name__ == "__main__":
    ## Keys Are Ready
    hotKeys = keyboard.GlobalHotKeys({
        '<shift>+-' : lambda: print("Add"),
        '<shift>+=' : lambda: print("Minus"),
        '<alt>+<shift>+f': lambda: print("Freeze"),
        'f' : lambda: print("Fill Text"),
        '<ctrl>+c': getFalse,
    })
    
    hotKeys.start()
    hotKeys.join()