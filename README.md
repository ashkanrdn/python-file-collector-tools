# Python File Collector Tools

Current Version: 2.0
Date: 3/9/2019
Creator: Jeffrey Lu

## Introduction
Collection of python scripts for collecting files across network drives and parsing their data to get information such as file version, creation date, and file creator.

# Usage
## Dynamo Tools

 1. Run `dynamocollector.py`to search the specified drive for files with `.dyn` file extensions.
 2. A `.csv` file with all collected file paths will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.
 3. Run `dynamoinfoparser.py` to retrieve relevant info for all collected files. 
 4. A new `.csv` file with all retrieved info will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.

## Grasshopper Tools

1. Run `grasshoppercollector.py`to search the specified drive for files with `.gh` file extensions.
 2. A `.csv` file with all collected file paths will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.
 3. Run `grasshopperinfoparser.py` to retrieve relevant info for all collected files. 
 4. A new `.csv` file with all retrieved info will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.

## Revit Tools

### RFA Collector
1. Run `rfacollector.py`to search the specified drive for files with `.rfa` file extensions.
 2. A `.csv` file with all collected file paths will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.
 3. Run `rfaversionparser.py` to retrieve relevant info for all collected files. 
 4. A new `.csv` file with all retrieved info will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.
 
### RVT Collector

1. Run `rvtcollector.py`to search the specified drive for files with `.rvt` file extensions.
 2. A `.csv` file with all collected file paths will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.
 3. Run `rvtversionparser.py` to retrieve relevant info for all collected files. 
 4. A new `.csv` file with all retrieved info will be saved in `C:\Logs\`. The `.csv` file name will begin with today's date.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE0NzMyNjc5XX0=
-->