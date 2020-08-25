## Selenium Note Taker

An Automated Note-Taking Software

![Gif](https://media.giphy.com/media/U51DcStRjNOTKFaznO/giphy.gif)
![Notes](https://github.com/harris222/Selenium-Note-Taker-/blob/master/Example%20Notes/Notes.PNG)

### HOWTO Use (IMPORTANT! READ IT ALL):
Launch a Chrome Browser by typing python knowItAll.py into the command line. Then, input in a name for the file into which you will output your notes.

After completing the above steps, you can begin selecting text in the browser and storing notes. Each note you take using an URL will be shown under the URL with that header, like this

    <Insert Picture Here>

You can configure your notes using key commands. See them here


### Some Imperfect Features:
- To take notes from a tab in which you did not initially launch your ChromeDriver, you must press <alt>+s to change to that tab (See <alt>+s).
    
- A User cannot reformat all indents they've accidentally indented one level too far. A TkInter Text Editor should allow the user to visualize their notes
    and reconfigure indents.


### HOWTO Important KeyCommands:
#### Output Notes Into File : '\<ctrl\>+c':
    Close Browser and write out notes to the file you specified.
### HOWTO KeyCommands to Configure Your Notes:
#### Add Indent : '\<shift\>+='
    Add An Indent Level.

#### Subtract Indent : '\<shift\>+-'
    Subtract An Indent Level.

#### Fill Text : '\<shift\>+t'
    Fill in a sentence that you did not select fully.

#### Print Knowledge : '\<shift\>+p'
    List the Current Knowledge that you have selected in the command line.

#### Pop : '\<esc\>'
    Remove the text you just highlighted. 

#### Freeze : '\<alt\>+\<shift\>+f'
    Freeze all note configuration commands, just in case if you want to do something else and avoid accidentally configuring your notes.

### Some General Usage Tips:
    - To remove a note, remember to not select it. Or else, it will be recorded
    again.

Thank you for taking your time to read the README. If you want to recommend some features, send me a private message, issue or pull request!
