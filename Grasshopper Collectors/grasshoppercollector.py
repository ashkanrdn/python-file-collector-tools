import os, datetime, csv

#initialize variables
writedate = datetime.date.today()
filetype = ".gh"
filedirs = []
excludedirs = []
server = "\\\\d-peapcny.net"
ghfiles = {}
ghpathcsv = os.path.join("C:\\Logs\\", str(writedate) + "_ghpaths.csv")


##known locations of grasshopper files
filedirs.append(os.path.join(server, "Enterprise", "S_Standards", "Create"))
filedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Committees"))
filedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Social"))
filedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Offices"))
filedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Practice-Areas"))
filedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Recruitment"))


filedirs.append(os.path.join(server, "Enterprise", "P_Projects"))

'''
#exclude locations
excludedirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin", "Committees", "Data Unit", "01_TEAMS", "AUTOMATION", "grasshopper Script Management", "All grasshopper Graphs"))
'''

if __name__ == "__main__":

    run = True
    while run:

        #collect paths
        for filedir in filedirs:
            print(f'Now accessing {filedir}')
            print(f'Please wait while searching for grasshopper files.')
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
                        ghfiles[os.path.join(r, file)] = file

        print(f'{len(ghfiles)} total grasshopper graphs collected.')

        #check if c:\logs exists
        if not os.path.exists("C:\\Logs"):
            os.makedirs("C:\\Logs")
        else:
            pass

        try: 
            #write collected paths to csv logfile
            with open(ghpathcsv, "w", newline = '', encoding="utf-8") as log:
                logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                logwrite.writerow(['File Name', 'Path'])
                for a,b in ghfiles.items():
                    logwrite.writerow([b,a])

            print(f'All grasshopper graph paths successfully logged.')
            print(f'See {ghpathcsv} for details')
            break

        except PermissionError:
            print(f'Error: permission denied - file may be open')
            break

        except UnicodeEncodeError:
            print(f'Error: encoding error')
            break



 
