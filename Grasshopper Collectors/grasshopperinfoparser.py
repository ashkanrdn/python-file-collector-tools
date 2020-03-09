import os, olefile, re, csv, time, datetime, sys, win32api, win32con, win32security
from os import stat

writedate = datetime.date.today()
ghpathcsv = os.path.join("C:\\Logs\\", str(writedate) + "_ghpaths.csv")
ghinfocsv = os.path.join("C:\\Logs\\", str(writedate) + "_ghinfo.csv")
gh_names, gh_paths, gh_cdates, gh_ctimes, gh_mdates, gh_mtimes, gh_owners = [], [], [], [], [], [], []


def get_gh_info(gh_file):

    gh_owner = "unknown"
    try:
        creationdate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(gh_file)))
        creationtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getctime(gh_file)))
        modifieddate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(gh_file)))
        modifiedtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getmtime(gh_file)))
    except:
        creationdate, creationtime, modifieddate, modifiedtime = "unknown", "unknown", "unknown", "unknown"
    try: 
        sd = win32security.GetFileSecurity(gh_file, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner ()
        owner_name, owner_domain, type = win32security.LookupAccountSid(None, owner_sid)
        gh_owner = f'{owner_domain}\\{owner_name}'
                
    except:
        pass

    return creationdate, creationtime, modifieddate, modifiedtime, gh_owner

if __name__ == "__main__":

    run = True
    while run:

        if os.path.exists(ghpathcsv):
            print(f'Now accessing {ghpathcsv}')
            with open(ghpathcsv, "r", newline = '', encoding="utf-8") as log:              
                csvread = csv.reader(log, delimiter = ',')
                next(csvread)
                for row in csvread:
                    filename = str(row[0])
                    filepath = str(row[1])
                    gh_names.append(filename)
                    gh_paths.append(filepath)
                    gh_cdates.append(get_gh_info(filepath)[0])
                    gh_ctimes.append(get_gh_info(filepath)[1])
                    gh_mdates.append(get_gh_info(filepath)[2])
                    gh_mtimes.append(get_gh_info(filepath)[3])
                    gh_owners.append(get_gh_info(filepath)[4])
                    print(filepath, get_gh_info(filepath)[4])

            print(f'{len(gh_paths)} grasshopper graphs logged')

            try:
                with open(ghinfocsv, "w", newline = '', encoding="utf-8") as log:
                    logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    logwrite.writerow(["File Name", "File Path", "Creation Date", "Creation Time", "Modified Date", "Modified Time", "File Owner"])
                    for a, b, c, d, e, f, g in zip(gh_names, gh_paths, gh_cdates, gh_ctimes, gh_mdates, gh_mtimes, gh_owners):
                        logwrite.writerow([a,b,c,d,e,f,g])

                print(f'All grasshopper graph information successfully logged.')
                print(f'See {ghinfocsv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break
        else:
            print(f'Error: run grasshopperpathcollector script first.')
            break