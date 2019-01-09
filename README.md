# High Intensity Peak Analysis


#### Beta


Calculates high intensity peaks from a given text file and creates  
different output files.  
Tested with text files provided by Fiji.  
Sample data is provided in the sampleData folder.  
Your data will probably work if the text file has the structure as the files in sampleData  
Important: each entry is divided by a Tabstop (\t)  
If the Tabstop is missing, the program will fail!

This tool uses Python 3.x. It's not tested with Python < 3.x. It is using a venv (virtual environment) to prevent missleading toolinstalltions or python installations.

Windows users should either install Cygwin or follow the manual installation (see Manual Installation)

## Dependencies

- See requirements.txt

## Installation

### Automatic Installation


- Download/Clone Repo
- type "sh run.sh" in your console
- Done

IMPORTANT: For an automatic installation you need support for sh Scripts. On Windows this can be achieved by installing Cygwin.

### Manual Installation

Mac/Unix:

- Start console/terminal on your local machine 
- Clone/Download Repo 
- Navigate to cloned/downloaded Repo
- Create Virtual Environment. *e.g.* by typing: "python -m venv ./venv" in your console
- Activate Environment. *e.g.* by typing: "source venv/bin/activate" in your console
- install requirements by typing: "pip install -r requirements.txt" in your console


Windows:
- Start Powershell on your local machine 
- Clone/Download Repo 
- Navigate to cloned/downloaded Repo
- Create Virtual Environment. *e.g.* by typing: "python -m venv ./venv" in your Powershell
- Activate Environment. *e.g.* by typing: "./venv/Scripts/activate" in your Powershell
- install requirements by typing: "pip install -r requirements.txt" in your Powershell

## Usage

Mac/Unix:

- sh start.sh

Windows:

- Run start.bat

### Manual usage

- Navigate to cloned/downloaded Repo
- Activate Environment. *e.g.* by typing: "source venv/bin/activate" in your console
- python3 start.py [Arguments] 
- e.g python start.py -D
---

***

## Command Line Arguments:

commands are only available when in manual usage!
- [-D / --debug]: Debug mode -> Logging lots of Data into Console(However, all Data is logged into the Logging Files)
- [-V / --verbose]: Verbose mode -> Verbose output of Calculations  
- [-H / --highintense]: Skips the main menu and jumps directly to the High Intensity Peak Analyzer Tool
- [-r / --restore]: Restores the default config.ini

You can combine several argument e.g 
python start.py -V -D. Program will start in Debug and Verbose Mode




## Copyright:
  Exitare  
  [Github](https://github.com/Exitare)  
  [Website](https://exitare.de)

  

## Sample Usage
- General: 
    1. python start.py [Arguments] e.g python start.py -D 
    2. Choose your preferred Actions
    3. Follow the Action steps


=======
>>>>>>> master

## Contributors
Kaya Keutler 

