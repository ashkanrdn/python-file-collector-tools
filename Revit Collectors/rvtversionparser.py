import os, olefile, re, csv, time, datetime, sys, win32api, win32con, win32security
from os import stat

write_date = datetime.date.today()
rvt_paths_csv = os.path.join("C:\\Logs\\", str(write_date) + "_rvtpaths.csv")
rvt_info_csv = os.path.join("C:\\Logs\\", str(write_date) + "_rvtinfo.csv")
rvt_names, rvt_paths, rvt_cdates, rvt_ctimes, rvt_mdates, rvt_mtimes, rvt_owners, rvt_versions, file_sizes = [], [], [], [], [], [], [], [], []


def get_rvt_info(rvt_file):
    rvt_version = "unknown"
    rvt_owner = "unknown"
    file_size = "unknown"
    try:
        creationdate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(rvt_file)))
        creationtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getctime(rvt_file)))
        modifieddate = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(rvt_file)))
        modifiedtime = time.strftime('%H:%M:%S', time.gmtime(os.path.getmtime(rvt_file)))
    except:
        creationdate, creationtime, modifieddate, modifiedtime = "unknown", "unknown", "unknown", "unknown"
    try: 
        sd = win32security.GetFileSecurity(rvt_file, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner ()
        owner_name, owner_domain, type = win32security.LookupAccountSid(None, owner_sid)
        rvt_owner = f'{owner_domain}\\{owner_name}'
        if olefile.isOleFile(rvt_file):
            try:
              rvt_ole = olefile.OleFileIO(rvt_file)
              rvt_bfi = rvt_ole.openstream("BasicFileInfo")
              rvt_file_info = str(rvt_bfi.read()).replace("\\x00", "")
              adesk_version_pattern = re.compile(r'Autodesk Revit \d{4}|Format..\d{4}')
              rvt_version = re.search(adesk_version_pattern, rvt_file_info)[0]
            except:
                pass
        else:
          print(f'file does not appear to be an ole file: {rvt_file}')
                
    except:
        pass

    try:
        file_size = os.path.getsize(rvt_file)

        if file_size < 1024*1024:
            file_size = str(round((file_size/1024), 2)) + "KB"
        else:
            file_size = str(round((file_size/1024/1024), 2)) + "MB"
    except:
        pass

    return creationdate, creationtime, modifieddate, modifiedtime, rvt_owner, rvt_version, file_size

if __name__ == "__main__":

    run = True
    while run:

        if os.path.exists(rvt_paths_csv):
            print(f'Now accessing {rvt_paths_csv}')
            with open(rvt_paths_csv, "r", newline = '', encoding="utf-8") as log:              
                csvread = csv.reader(log, delimiter = ',')
                next(csvread)
                for row in csvread:
                    filename = str(row[0])
                    filepath = str(row[1])
                    rvt_names.append(filename)
                    rvt_paths.append(filepath)
                    rvt_cdates.append(get_rvt_info(filepath)[0])
                    rvt_ctimes.append(get_rvt_info(filepath)[1])
                    rvt_mdates.append(get_rvt_info(filepath)[2])
                    rvt_mtimes.append(get_rvt_info(filepath)[3])
                    rvt_owners.append(get_rvt_info(filepath)[4])
                    rvt_versions.append(get_rvt_info(filepath)[5])
                    file_sizes.append(get_rvt_info(filepath)[6])
                    print(filepath, get_rvt_info(filepath)[5], get_rvt_info(filepath)[0])

            print(f'{len(rvt_paths)} rvt files logged')
            print(rvt_versions)

            try:
                with open(rvt_info_csv, "w", newline = '', encoding="utf-8") as log:
                    logwrite = csv.writer(log, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    logwrite.writerow(["File Name", "File Path", "Creation Date", "Creation Time", "Modified Date", "Modified Time", "File Owner", "File Version", "File Size"])
                    for a, b, c, d, e, f, g, h, i in zip(rvt_names, rvt_paths, rvt_cdates, rvt_ctimes, rvt_mdates, rvt_mtimes, rvt_owners, rvt_versions, file_sizes):
                        logwrite.writerow([a,b,c,d,e,f,g,h,i])
                        

                print(f'All rvt file information successfully logged.')
                print(f'See {rvt_info_csv} for details')
                break

            except PermissionError:
                print(f'Error: permission denied - file may be open')
                break
        else:
            print(f'Error: run rvtpathcollector script first.')
            break