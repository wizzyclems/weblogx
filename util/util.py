#!/usr/bin/env python3

from datetime import datetime
import subprocess


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

def testMethod():
    if((J2>60),">1hour",if((J2>30),">30min",if((J2>20),">20mins",if((J2>15),">15mins",if((J2>10),">10mins",if((J2>5),">5mins",if((J2>3),">3mins",if((J2>1),">1min",
if((J2<1),"1 min","Bad Date")))))))))