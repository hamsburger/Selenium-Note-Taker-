# Selenium Note Taker 📝 An Automated Note-Taking Software

### Guide Link
![Gif](https://media.giphy.com/media/U51DcStRjNOTKFaznO/giphy.gif)

&nbsp;
## HOWTO Use (IMPORTANT! READ IT ALL):
Launch a Chrome Browser by launching this command in the command line in your root directory. 

```
python knowItAll.py
```

Wait for Chrome Driver to Launch. Then, the program will prompt for the name of your output file,
which will contain the output of your notes.

After completing the above steps, you can begin [**highlighting** text](https://github.com/harris222/Selenium-Note-Taker-/blob/master/README.md#guide-link) in the browser and store notes. Each note you take using an URL will be shown under the URL with that header, like this

![Notes](https://github.com/harris222/Selenium-Note-Taker-/blob/master/Example%20Notes/Notes.PNG)

You can configure your notes using key commands. [See them here](https://github.com/harris222/Selenium-Note-Taker-/blob/master/README.md#howto-important-keycommands)

&nbsp;
## Some Imperfect Features:
- To take notes from a tab in which you did not initially launch your ChromeDriver, you must press \<alt\>+s to change to that tab ([See \<alt\>+s](https://github.com/harris222/Selenium-Note-Taker-/blob/master/README.md#change-window-handle)).
- Note printing prints out a python list, which is not human-readable. 
- A User cannot reformat all indents they've accidentally indented one level too far. A TkInter Text Editor should allow the user to visualize their notes
    and reconfigure indents.

&nbsp;
## HOWTO Important KeyCommands:
### Output Notes Into File : '\<ctrl\>+c':
Close Browser and write out notes to the file you specified.

### Print Knowledge : '\<shift\>+p'
Print out notes that you have selected in the command line.

#### Change Window Handle : '\<alt\>+s'
Switch to a New Tab. Index 1 for first tab, 2 for second tab, 
... and N for Nth Tab. 

&nbsp;
## HOWTO KeyCommands to Configure Your Notes:
### Add Indent : '\<shift\>+='
Add An Indent Level.

### Subtract Indent : '\<shift\>+-'
Subtract An Indent Level.

### Fill Text : '\<shift\>+t'
Fill in a sentence that you did not finish selecting.

### Pop : '\<esc\>'
Remove the text you just highlighted. 

### Freeze : '\<alt\>+\<shift\>+f'
Freeze all note configuration commands, just in case if you want to do something else and avoid accidentally configuring your notes.

&nbsp;
## Some General Usage Tips:
- To remove a note, remember to not select it. Or else, it will be recorded
again. ([Understand the Features](https://github.com/harris222/Selenium-Note-Taker-/blob/master/README.md#howto-use-important-read-it-all))

Thank you for taking your time to read the README. If you want to recommend some features, send me a private message, issue or pull request!
