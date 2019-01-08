# High Intensity Peak Analysis


#### Beta


Calculate high intensity Peaks from a given file and creates  
different output files.  
Tested with files provided by Fiji.  
Sample Data is provided in sampleData Folder.  
Your data might work if the txt is the structure as the files in sampleData.  
Important: Each entry is divided by a Tabstop (\t)  
If the Tabstop is missing, the program will fail!


## Dependencies

- See requirements.txt


## Installation
- Install Python 3.x
- Download/Clone Repo
- sh run.sh
- Done

### Manual 

- Create Virtual Environment. e.g. python -m venv ./venv
- Activate Environment. e.g source venv/bin/activate
- pip install -r requirements.txt




## Usage

- sh run.sh


---

Optional:

- python3 start.py [Arguments] 
- e.g python start.py -D 


***
Important notice:  
A path with multiple or a single blank is not recommended!
High Intensity Peak Analysis will try to fix the path but this isn´t a 
100% chance that it will work

## Command Line Arguments:

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



  
## Contributors:
    

