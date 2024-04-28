# Python Desktop and Downloads Cleaner

This Python project provides 3 scripts used for automating cleaning of your desktop and downloads folders. It organizes files into specified directories based on their extensions and creates folders titled with year and month for better organization of the cleaned files. Depending on the script, cleaner.py allows user to choose wether they want to clean their desktop or downloads folder while the desktop_cleaner.py and downloads_cleaner.py were created with the intention of being run in the background.

## Features
- Moves files from the desktop and/or downloads folders to appropriate directories created on desktop
- Automatically creates year_month folders for better file organization
- Supports cleaning of various file types including text, images, audio, video, compressed files, and more
- 2 scripts that can easily be run in the background to clean either desktop or downloads folder

## Setup
1. Clone the repository
2. Install the required dependencies using pip:
```bash
 pip install watchdog 
```
3. Run the script:
- Open a terminal
- Navigate to the directory where the script is located
- Run the script using Python:
```bash
python cleaner.py 
```

## Running in the Background
### Windows
To run the script in the background on Windows you can use ***pythonw.exe***

1. Open cmd
2. Navigate to the directory containing ***desktop_cleaner.py*** or ***downloads_cleaner.py*** script
3. Run the script using ***pythonw.exe***:
```bash

pythonw.exe desktop_cleaner.py

```

The script will now run continuously in the background, organizing your desktop files as they are added or modified.

### Linux
On Linux systems you can use the ***nohup*** to run scripts in the background

1. Open terminal
2. Navigate to the directory containing ***desktop_cleaner.py*** or ***downloads_cleaner.py*** script
3. Run the script using ***nohup***:
```bash

nohup python3 desktop_cleaner.py &

```
Similarly to running in Windows script will now run continuously in the background, organizing your desktop files as they are added or modified.
***nohup*** command prevents the script from being terminated when you log out or close the terminal, to stop the script running in the background find PID and terminate it.
Example for desktop_cleaner.py:
```bash
ps aux | grep desktop_cleaner.py

```
then use ***kill*** command on the process ID.



