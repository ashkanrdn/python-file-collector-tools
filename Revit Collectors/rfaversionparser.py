import os, olefile, re, csv, time, datetime, sys, win32api, win32con, win32security
from os import stat

write_date = datetime.date.today()
rfa_paths_csv = os.path.join("C:\\Logs\\", str(write_date) + "_rfapaths.csv")
rfa_info_csv = os.path.join("C:\\Logs\\", str(write_date) + "_rfainfo.csv")
rfa_names, rfa_paths, rfa_cdates, rfa_ctimes, rfa_mdates, rfa_mtimes, rfa_owners, rfa_versions = [], [], [], [], [], [], [], []


def get_rfa_info(rfa_file):
    rfa_version = "unknown"
    rfa_owner = "unknown"
    try:
        creationdate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(rfa_file)))
        creationtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getctime(rfa_file)))
        modifieddate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(rfa_file)))
        modifiedtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getmtime(rfa_file)))
    except:
        creationdate, creationtime, modifieddate, modifiedtime = "unknown", "unknown", "unknown", "unknown"
    try: 
        sd = win32security.GetFileSecurity(rfa_file, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner ()
        owner_name, owner_domain, type = win32security.LookupAccountSid(None, owner_sid)
        rfa_owner = f'{owner_domain}\\{owner_name}'
        if olefile.isOleFile(rfa_file):
            try:
              rfa_ole = olefile.OleFileIO(rfa_file)
              rfa_bfi = rfa_ole.openstream("BasicFileInfo")
              rfa_file_info = str(rfa_bfi.read()).replace("\\x00", "")
              adesk_version_pattern = re.compile(r'Autodesk Revit \d{4}|Format..\d{4}')
              rfa_version = re.search(adesk_version_pattern, rfa_file_info)[0]
            except:
                pass
        else:
          print(f'file does not appear to be an ole file: {rfa_file}')
                
    except:
        pass

    return creationdate, creationtime, modifieddate, modifiedtime, rfa_owner, rfa_version

if __name__ == "__main__":

    run = True
    while run:

        if os.path.exists(rfa_paths_csv):
            print(f'Now accessing {rfa_paths_csv}')
            with open(rfa_paths_csv, "r", newline = '', encoding="utf-8") as log:              
                csvread = csv.reader(log, delimiter = ',')
                next(csvread)
                for row in csvread:
                    filename = str(row[0])
                    filepath = str(row[1])
                    rfa_names.append(filename)
                    rfa_paths.append(filepath)
                    rfa_cdates.append(get_rfa_info(filepath)[0])
                    rfa_ctimes.append(get_rfa_info(filepath)[1])
                    rfa_mdates.append(get_rfa_info(filepath)[2])
                    rfa_mtimes.append(get_rfa_info(filepath)[3])
                    rfa_owners.append(get_rfa_info(filepath)[4])
                    rfa_versions.append(get_rfa_info(filepath)[5])
                    print(filepath, get_rfa_info(filepath)[5], get_rfa_info(filepath)[0])

            print(f'{len(rfa_paths)} rfa files logged')
            print(rfa_versions)

            try:
                with open(rfa_info_csv, "w", newline = '', encoding="utf-8") as log:
                    logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    logwrite.writerow(["File Name", "File Path", "Creation Date", "Creation Time", "Modified Date", "Modified Time", "File Owner", "File Version"])
                    for a, b, c, d, e, f, g, h in zip(rfa_names, rfa_paths, rfa_cdates, rfa_ctimes, rfa_mdates, rfa_mtimes, rfa_owners, rfa_versions):
                        logwrite.writerow([a,b,c,d,e,f,g,h])
                        

                print(f'All rfa file information successfully logged.')
                print(f'See {rfa_info_csv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break
        else:
            print(f'Error: run rfapathcollector script first.')
            break