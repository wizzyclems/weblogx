#!/usr/bin/env python3

from datetime import datetime
import subprocess
import os
import shutil


def getAppProperties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value
    return props


def formatDate(date):
    return datetime.today().strftime('%Y-%m-%d')


def backupFile(oldLocation, newLocation):
    subprocess.call(["mv", oldLocation, newLocation])
    print("file move completed")


def backupLogFile(backup_location, file):
  #subprocess.call(["mv", log_location + "/" + file, backup_location + "/" + file])
  print("Attempting backup of the processed log file...")

  #check if the backup location exist. If it does not, create it.
  if not os.path.exists(backup_location):
    os.makedirs(backup_location)
  
  shutil.move(file, backup_location)
  print("File backup completed")


# create chunker function to separate the dataframe into batches
# Note: last batch will contain smallest amout of records.
def chunker( dataList, size):
    return( dataList[pos:pos+size] for pos in range(0,len(dataList),size) )


def testMethod():
    pass
    #if((J2>60),">1hour",if((J2>30),">30min",if((J2>20),">20mins",if((J2>15),">15mins",if((J2>10),">10mins",if((J2>5),">5mins",if((J2>3),">3mins",if((J2>1),">1min",if((J2<1),"1 min","Bad Date")))))))))