# Python File Collector Tools

Current Version: 2.0
Date: 3/9/2019
Creator: Jeffrey Lu

## Introduction
Collection of python scripts for collecting files across network drives and parsing their data to get information such as file version, creation date, and file creator.

# Usage

A note on usage: **the collector tools take a long time to run**. Be patient. Do not run the collector tools during work hours to avoid any negative impact to the network. I usually will run the collector tool overnight and then run the info parser the next morning.

Always run the collector tool first and *then* the info parser.

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
eyJoaXN0b3J5IjpbLTE3NTc2MDUxNTgsLTE0NzMyNjc5XX0=
-->