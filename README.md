# High Intensity Peak Analysis (HIPA) tool


## Summary

This tool enables for faster analysis of continously recoreded (fluorescence)-intensity data pre-processed in FIJI. 
The tool reads .txt files generated with FIJI. Following data import, the tool will perform data normalization based on the maximal intensity, compute the number of high intensity events based on a user-set threshold and perform signal comparisons within one set of data. After analysis the tool will generate the following output files, which can then be imported in any data manipulation software for further analysis such as plotting etc:
1. normalized data
2. count of high intensity events, based on the user-set threshold per minute 
3. average of high intensity events, based on the user-set threshold per minute and cell
4. comparison of intensity values between user-defined intervals as well as between each interval and the baseline (the tool will check for activated cell aka cells that show higher intensity values compared to baseline and/or the previous interval). 

So far, the tool has been tested with text files provided by FIJI. Sample data is provided in the sampleData folder.  
Your data will probably work if the text file has the structure as the files in sampleData  
Important: each entry is divided by a Tabstop (\t)  
If the Tabstop is missing, the program will fail!
This tool uses Python 3.x. It's not tested with Python < 3.x. It is using a venv (virtual environment) to prevent misleading toolinstalltion or python installations.


## Dependencies

- See requirements.txt

## Installation

### Automatic Installation


- Download/Clone Repo
- Navigate to the folder where the Repo is stored.
- Execute ```start.bat``` (Windows) or enter  ```./start.sh``` in your Terminal/Console (Mac)
- Done

IMPORTANT: Automatic Installation and Execution prevents you from using the CommandLine Arguments.


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
- Activate Environment. *e.g.* by typing: Unix/Mac: "source venv/bin/activate" / Windows: "./venv/Scripts/activate" in your console/shell
- python HIPA.py [Arguments] 
- e.g python HIPA.py -D

## Command Line Arguments:

commands are only available when in manual usage!
- [-D / --debug]: Debug mode -> Logging lots of Data into Console (However, all Data is logged into the Logging Files)
- [-V / --verbose]: Verbose mode -> Verbose output of Calculations  
- [-H / --highintense]: Skips the main menu and jumps directly to the High Intensity Peak Analyzer Tool
- [-r / --restore]: Restores the default config.ini

You can combine several argument e.g 
python start.py -V -D. Program will start in Debug and Verbose Mode

## Detailed procedure

### Data requirements
In order to make use of the HIPA tool, one has to pre-process their imaging data using FIJI. In FIJI the experimenter can perform any data manipulation wished for as long as the final intensity values are stored in a .txt files with cells as columns and frame numbers as rows. *note*: This tools is based on a duration of 3.9 seconds per frame. If you use longer or shorter frame times the calculations will be off!
The tool comes with a Data folder, into which the experimenter is expected to load any .txt files he wishes to be analyzed. The tool will recognize any .txt file starting with time_traces_YOURTEXTHERE.txt
After analysis, all generated output files are to be found in the results folder.

### Operating the HIPA tool
The tool will recognize all .txt files in the raw data folder and automatically import them for analysis. For each .txt file the tool will request:
- the frame number(s) at which additions took place (if multiple additions were performed, please separate the frame numbers by comma)
- the threshold the user whishes to set (must be between 0 and 1). *note*: the threshold can be interpreted as a cut-off value. It may be different among experiments and it has to be set empirically and depends on the data judgement by the experimenter. If a threshold of 0.6 is set it means that the tool will calculate the intensity value that corresponds to 60 % of the maximum value and will count anything greater or equal to that value as an high intensity event. Hence, where the threshold is set determines how much signal and/or noise is counted. Therefore, it makes sense to perform a baseline as well as a maximum reading during the duration of the experiment and place the treshold accoringly.

#### Normalization
The tool will normalize the imported data as the first step of analysis. The data will be normalized between 0 and 1.

#### Calculation of high intensity events
Based on the threshold that has been set by the user, the tool will only count values that are greater or equal to that threshold. These counts represent the high intensity events and are computed on a per minute basis for each cell. The tool will also generate an average overview of the data by by summarizing all high intensity events and deviding by the number of cells; hence generating a high intensity event count per minute per cell.

#### Interval comparison
An interval defines the time from the start of the recording until the first addition of a stimulus as well as the time in between subsequent additions. The intervals are defined for each imported .txt files by listing the addition frame numbers when prombted. For each of the listed intervals the tool will perform a comparison to the baseline (the baseline is considered as the recording time before the first addition) as well as towards each previous interval if multiple additions where performed. The tool is designed to identify an activation of the cell aka an increase in high intensity events per minute compared to the baseline or the previous interval. If that is to be the case the tool will mark that cell as True in the given interval. Otherwise it will be listed as False.

## Copyright:
  Exitare  
  [Github](https://github.com/Exitare)  
  [Website](https://exitare.de)

  

## Contributors
  [KayaHub](https://github.com/KayaHub)  

