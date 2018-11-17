# High Intensity Peak Analysis


Calculate high intensity Peaks from a given file.  
Tested with files provided by Fiji.  
Sampledata is provided in sampleData Folder.  
Your data might work if the txt is the structure as the files in sampleData.  
Important: Each entry is divided by a Tabstop (\t)  
If the Tabstop is missing, the program will fail!


## Dependencies

- See requirements.txt


## Installation
- Install Python 3.x
- Download Repo
- Optional: Create Virtual Environment. e.g. python3 -m venv ./venv
- Optional: Activate Environment. e.g source venv/bin/activate
- pip install -r requirements.txt
- Done



## Usage

1. python start.py [Arguments] e.g python start.py -D 
2. Choose your preferred Actions
3. Follow the Action steps



## Command Line Arguments:

- [-D / --debug]: Debug mode -> Logging lots of Data into Console(However, all Data is logged into the Logging Files)
- [-V / --verbose]: Verbose mode -> Verbose output of Calculations  
- [-h / --highintense]: Skips the Mainmenu and jumps directly to the High Intensity Peak Analyzer Tool
- [-r / --restore]: Restores the default config.ini




## Copyright:
  Exitare  
  [Github](https://github.com/Exitare)  
  [Website](https://exitare.de)
  
  
## Contributors:
    