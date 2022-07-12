import os
import json
from datetime import datetime

def searchfiles(filename, type=None):
    with open('filelog.json', 'r') as filedb:
        try:
            fdict = json.load(filedb)
        except:
            log_all_files()
    if type == None:
        try:
            return fdict['exe'][filename.lower()]
        except:
            #print("it moves on...")
            choicep = []
            choicen = []
            for file in fdict['exe']:
                if filename.lower() in file:
                    choicep.append(fdict['exe'][file])
                    choicen.append(file)
            return(choicep)


def log_all_files(filetype=['exe', 'py', 'lnk']):
    date = datetime.now()
    drives = ['C:\\', 'E:\\', f'C:\\Users\\{os.getlogin()}']
    fldict = {'exe': {}, 'gen': {}}
    with open("preferences.json", "r") as lfile:
        try:
            ldict = json.load(lfile)
            old_date = datetime.strptime(ldict['last_log'].split('.')[0], "%Y-%m-%d %H:%M:%S")
            diff = str(date - old_date)
            #print(diff)
        except Exception as e:
            diff = "day"
    if 'day' in diff:
        with open("preferences.json", "w+"):
            wdict = {"last_log": str(date)}
            for drive in drives:
                exclude = set(['Users'])
                for root, dirs, files in os.walk(drive, topdown=True):
                    dirs[:] = [d for d in dirs if d not in exclude]
                    for file in files:
                        if file.split('.')[-1] in filetype:
                            #print(root+'\\'+file)
                            if file.endswith('.exe'):
                                fldict['exe'][file.split('.exe')[0].lower()] = root + "\\"+ file
                            elif file.endswith('.lnk') and root == "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs":
                                    fldict['exe'][file.split('.lnk')[0].lower()] = root + "\\"+ file
                            else:
                                fldict['gen'][file.split('.')[0].lower()] = root + "\\"+ file
        with open("filelog.json", "w+") as jfile:
            json.dump(fldict, jfile)


#log_all_files()