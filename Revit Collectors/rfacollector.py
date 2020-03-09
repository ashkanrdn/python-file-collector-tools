import os, datetime, csv

#initialize variables
write_date = datetime.date.today()
file_type = ".rfa"
file_dirs = []
exclude_dirs = []
server = "\\\\d-peapcny.net"
rfa_files = {}
rfa_paths_csv = os.path.join("C:\\Logs\\", str(write_date) + "_rfapaths.csv")


#known locations of Revit files
#file_dirs.append(os.path.join(server, "Enterprise", "S_Standards", "Create"))
file_dirs.append(os.path.join(server, "Enterprise", "G_Gen-Admin"))
file_dirs.append(os.path.join(server, "Enterprise", "P_Projects"))

'''
#exclude locations
exclude_dirs.append(os.path.join())
'''

if __name__ == "__main__":

    run = True
    while run:

        #collect paths
        for file_dir in file_dirs:
            print(f'Now accessing {file_dir}')
            print(f'Please wait while searching for Revit families.')
            for r, d, f, in os.walk(file_dir):
                [d.remove(dir) for dir in list(d) if dir in exclude_dirs]
                for file in f:
                    if str(file).endswith(file_type):
                        long_name = os.path.join(r,file)
                        print(r,file)
                        if len(long_name) > 259:
                            for_cmd = 'for %I in ("' + long_name + '") do echo %~sI'
                            p = os.popen(for_cmd)
                            file = p.readlines()[-1].rstrip()
                        else:
                            pass
                        rfa_files[os.path.join(r, file)] = file

        print(f'{len(rfa_files)} total Revit families collected.')

        #check if c:\logs exists
        if not os.path.exists("C:\\Logs"):
            os.makedirs("C:\\Logs")
        else:
            pass

        #check if log file exists
        if not os.path.exists(rfa_paths_csv):
            try:
                #write collected paths to new csv logfile
                with open(rfa_paths_csv, "w", newline = '', encoding="utf-8") as log:
                    log_write = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    log_write.writerow(['File Name', 'Path'])
                    for a,b in rfa_files.items():
                        log_write.writerow([b,a])

                print(f'All Revit family paths successfully logged.')
                print(f'See {rfa_paths_csv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break

            except UnicodeEncodeError:
                break

        #if log file exists 
        elif os.path.exists(rfa_paths_csv):
            print("exists")
            try:
                #add collected paths to existing csv logfile
                with open(rfa_paths_csv, "a", newline = '', encoding="utf-8") as log:
                    log_write = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    for a,b in rfa_files.items():
                        log_write.writerow([b,a])

                print(f'All Revit family paths successfully logged.')
                print(f'See {rfa_paths_csv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break

            except UnicodeEncodeError:
                break



 
