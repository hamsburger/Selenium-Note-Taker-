from pynput import keyboard
from pynput.keyboard import Key, Controller 



## Update urlKnowledge, url, currBaseText in Real Time (Setter)
## Update Level on Keypress  
# class keyThread:

def handleTabLevel(driver, level):
    '''
    '''
        ## Tabbing Level
    if keyboard.read_key() == "shift+-":
        if level > 0:
            level -= 1
        print("shift+-")
        if __name__ != "__main__":
            driver.alert("Current Level: " + str(level))
        


    elif keyboard.read_key() == 'shift+=':
        level += 1
        print("shift+=")
        if __name__ != "__main__":
            driver.alert("Current Level: " + str(level))
    
    

    return level
def handleOperation(driver, urlKnowledge, url, currBaseText):
    '''
    '''

    print(keyboard.read_key())
    ## Pop Last Element Inserted
    if keyboard.read_key() == 'esc':
        if len(urlKnowledge[url]) != 0:
            poppedString = "Pop " + urlKnowledge[url].pop()["detail"]
            driver.alert(poppedString)
            return

        driver.alert("Can't Pop. No Knowledge In The List")
    ## Fill Word
    elif keyboard.read_key() == 'shift+f':
        if len(urlKnowledge[url]) == 0:
            return 

        recentKnowledge = urlKnowledge[url][len(urlKnowledge[url]) - 1]["detail"]
        searchF = re.search(recentKnowledge.lower(), currBaseText)
        print(recentKnowledge, currBaseText)
        if searchF == None:
            return 

        start = searchF.start()
        end = searchF.end()
        newStart, newEnd = traverseTillSpace(start, end, currBaseText, recentKnowledge)
        urlKnowledge[url][len(urlKnowledge[url]) - 1]["detail"] = currBaseText[newStart:newEnd]
        driver.alert("Text formatted from: " + recentKnowledge + " to " + urlKnowledge[url][len(urlKnowledge[url]) - 1]["detail"])

def activateHotKeys():  
    def addLevel():
        print('Add Level!')

    def subtractLevel():
        print('Subtract Level!')

    def fillText():
        print('Fill Text!')

    def pop():
        print('Pop')
        
    def stop():
        h.stop()
 
    ## Keys Are Ready
    with keyboard.GlobalHotKeys({
        '<shift>+-' : subtractLevel,
        '<shift>+=' : addLevel,
        '<shift>+f' : fillText, 
        '<esc>' : pop,
        '<ctrl>+c': stop, 
    }) as h:
        h.join()

if __name__ == "__main__":
    activateHotKeys()