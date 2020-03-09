import os, olefile, re, csv, time, datetime, sys, win32api, win32con, win32security
from os import stat

writedate = datetime.date.today()
dynpathcsv = os.path.join("C:\\Logs\\", str(writedate) + "_dynpaths.csv")
dyninfocsv = os.path.join("C:\\Logs\\", str(writedate) + "_dyninfo.csv")
dyn_paths, dyn_versions, dyn_cdates, dyn_ctimes, dyn_mdates, dyn_mtimes, dyn_owners = [], [], [], [], [], [], []


def get_dyn_file_version(dyn_file):

    dyn_version = "unknown"
    dyn_owner = "unknown"
    try:
        creationdate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(dyn_file)))
        creationtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getctime(dyn_file)))
        modifieddate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(dyn_file)))
        modifiedtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getmtime(dyn_file)))
    except:
        creationdate, creationtime, modifieddate, modifiedtime = "unknown", "unknown", "unknown", "unknown"
    try: 
        with open(dyn_file, "r", encoding='UTF-8') as file:
            for line in file:
                if 'Workspace Version' in line:
                    dyn_version = line.split('"')[1]
                elif '"Version":' in line:
                    dyn_version = line.split('"')[3]
        sd = win32security.GetFileSecurity(dyn_file, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner ()
        owner_name, owner_domain, type = win32security.LookupAccountSid(None, owner_sid)
        dyn_owner = f'{owner_domain}\\{owner_name}'
                
    except:
        pass

    return dyn_version, creationdate, creationtime, modifieddate, modifiedtime, dyn_owner

if __name__ == "__main__":

    run = True
    while run:

        if os.path.exists(dynpathcsv):
            print(f'Now accessing {dynpathcsv}')
            with open(dynpathcsv, "r", newline = '') as log:              
                csvread = csv.reader(log, delimiter = ',')
                next(csvread)
                for row in csvread:
                    filename = str(row[1])
                    dyn_paths.append(filename)
                    dyn_versions.append(get_dyn_file_version(filename)[0])
                    dyn_cdates.append(get_dyn_file_version(filename)[1])
                    dyn_ctimes.append(get_dyn_file_version(filename)[2])
                    dyn_mdates.append(get_dyn_file_version(filename)[3])
                    dyn_mtimes.append(get_dyn_file_version(filename)[4])
                    dyn_owners.append(get_dyn_file_version(filename)[5])
                    print(filename, get_dyn_file_version(filename)[0])

            print(f'{len(dyn_paths)} dynamo graphs logged')

            try:
                with open(dyninfocsv, "w", newline = '') as log:
                    logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    logwrite.writerow(["File Path", "File Version", "Creation Date", "Creation Time", "Modified Date", "Modified Time", "File Owner"])
                    for a, b, c, d, e, f, g in zip(dyn_paths, dyn_versions, dyn_cdates, dyn_ctimes, dyn_mdates, dyn_mtimes, dyn_owners):
                        logwrite.writerow([a,b,c,d,e,f,g])

                print(f'All dynamo graph information successfully logged.')
                print(f'See {dyninfocsv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break
        else:
            print(f'Error: run dynamocollector script first.')
            break