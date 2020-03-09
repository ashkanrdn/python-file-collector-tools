import os, datetime, csv

#initialize variables
writedate = datetime.date.today()
filetype = ".dyn"
filedirs = []
excludedirs = []
server = "\\\\d-peapcny.net"
dynfiles = {}
dynpathcsv = os.path.join("C:\\Logs\\", str(writedate) + "_dynpaths.csv")
counter = 1;

filedirs.append(os.path.join(server, "Enterprise", "P_Projects"))

'''
#exclude locations
excludedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Committees", "Data Unit", "01_TEAMS", "AUTOMATION", "Dynamo Script Management", "All Dynamo Graphs"))
'''

if __name__ == "__main__":

    run = True
    while run:

        #collect paths
        for filedir in filedirs:
            print(f'Now accessing {filedir}')
            print(f'Please wait while searching for dynamo files.')
            for r, d, f, in os.walk(filedir):
                [d.remove(dir) for dir in list(d) if dir in excludedirs]
                for file in f:
                    if str(file).endswith(filetype):
                        long_name = os.path.join(r,file)
                        print(r,file)
                        if len(long_name) > 259:
                            for_cmd = 'for %I in ("' + long_name + '") do echo %~sI'
                            p = os.popen(for_cmd)
                            file = p.readlines()[-1].rstrip()
                        else:
                            pass
                        dynfiles[os.path.join(r, file)] = file

        print(f'{len(dynfiles)} total dynamo graphs collected.')

        #check if c:\logs exists
        if not os.path.exists("C:\\Logs"):
            os.makedirs("C:\\Logs")
        else:
            pass

        try: 
            #write collected paths to csv logfile
            with open(dynpathcsv, "w", newline = '') as log:
                logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                logwrite.writerow(['File Name', 'Path'])
                for a,b in dynfiles.items():
                    logwrite.writerow([b,a])

            print(f'All dynamo graph paths successfully logged.')
            print(f'See {dynpathcsv} for details')
            break

        except PermissionError:
            print(f'Error: permission denied - file may be open')
            break



 
