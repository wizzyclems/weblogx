#!/usr/bin/env python

import re
import operator
import csv
import os
from datetime import datetime
import subprocess
import shutil
import sys
from util import getAppProperties
from entity.LogLine import LogLine

log_location = "logs"
backup_location = "logs/backup"
connection = None
matchedRowCount = 0
#regex = r'^([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3})[ a-z:]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})[ a-z:\-\[]*(\d{1,2}/\w{3}/\d{4}):(\d{1,2}:\d{1,2})[ 0-9a-z:\]\+\"]*([A-Z]+)[ ]*([/\w-]+)[\w\W]*[A-Z]{4,5}[/\d\.\"]+ (\d{3,4})'
regex = r'\[([\d]{1,2}/[\w]{3,3}/[\d]{2,4}):([\d]{1,3}:[\d]{1,3}).*]\s([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\s([\w\d\.\-]*)\s([A-Z\d\-]*)\s\"([A-Z]{0,4})\s?([\w\d/\-\.]*)\s?([\w\d/\-\.]*)\"\s?([\d\-]*)\s?([\w\.]*)\s?([\d\-]*)\s?([\w\d/\-\.:]*)'
error_log_regex = r'^(\d{4}/\d{1,2}/\d{1,2}) (\d{1,2}:\d{1,2}).*client: ([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}).*request: \"([A-Z]+) ([/\w-]+).*upstream: \"[a-z:/]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})'
logList = []
channel = ""
header_set = False


def loadDB():
  return createPostgresDBConnection()


def read_SSL_Log(file):
  global logList
  fileRowCount = 0
  global matchedRowCount
  logList = []
  
  with open(file, mode='r') as log:
    for line in log.readlines():

      fileRowCount = fileRowCount + 1
      result = re.search(regex, line)

      if result == None :
        print("No match found for row {}".format(fileRowCount))
        print(line)
        continue

      if result.groups() < 12 :
        print("The log line is not a complete one with group size {}".format(result.groups()))
        print(result.groups())
        continue

      #request = result.group(7)
      #if "/biocapture/config/settings" in request:
      #  request = "/biocapture/config/settings"

      #if "/biocapture/resync" in request:
      #  request = "/biocapture/resync"

      #logList.append( (datetime.today(),result[1],result[2],result[3],request,'172.16.5.232') )
      #below line packs the request items into a tuple and append the tuple to the list
      #logList.append( (result.group(1),result.group(2),result.group(3),result.group(4),result.group(5), result.group(6),request, result.group(8), channel ) )
      
      logLine = LogLine()
      logLine.setRequestDate(result.group(1))
      logLine.setRequestTime(result.group(2))
      logLine.setSourceIp(result.group(3))
      logLine.setSecurityProtocol(result.group(4))
      logLine.setCypherSuite(result.group(5))
      logLine.setRequestMethod(result.group(6))
      logLine.setRequest(result.group(7))
      logLine.setHttpVersion(result.group(8))
      logLine.setRequestSize(result.group(9))
      logLine.setRequestHost(result.group(10))
      logLine.setResponseStatusCode(result.group(11))
      logLine.setResponseServer(result.group(12))
      logLine.setChannel(channel)

      logList.append(logLine.__str__())

      matchedRowCount = matchedRowCount + 1
      
    log.close()

  print("The file row count is {}".format(fileRowCount))
  print("The matched row count is {}".format(matchedRowCount))


def loadLogs():
  
  try:
    log_files = os.listdir(log_location) 
  except(OSError ):
    print("Error encountered while trying to read from the log location. Kindly confirm the log location path is correct and try again.")
    print("Terminating the application now...")
    exit()
  
  
  #TODO - write into a file the name of the last log file read so as to not read it again. You can also write the names the last 50 logs files read.
  for log in log_files:
    
    # skip the file if it is not an ssl or ssl-error log file.
    if ("ssl" not in log) and ("error" not in log) :
       continue

    # skip the log file if it is zipped.
    #TODO I think it would be useful to implement reading of zipped log files
    if ".gz" in log :
      print (log)
      continue

    # Read and process ssl logs
    if "ssl" in log :
      #reading successful SSL logs
      print(log)
      read_SSL_Log(log_location + "/" + log)

      #below line inserts each log entry into an Oracle database
      #writeManySSLLogs(connection, logList)
      #print(logList)
      print("File processing done.")
      #generateReport()
      #print("Row count for file {} is {}".format(log_location + "/" + log, rowCount))

    # Read and process ssl-error logs. 
    # TODO add implementation for processing ssl-error logs
    if "ssl-error.log" in log :
      #reading successful SSL logs
      print("No suppport yet for reading SSL error log files")
      continue      

      #below line backs up the logfilethat was processed
    
    # Once reading and processing logs are complete, backup the log file in the specified location.
    #backupLogFile(log)
    
    
def generateReport():
  global header_set
  
  if not header_set :
    logList.insert(0,("source_ip","destination_ip","destination_port","request_date","request_time","request_method","request","response_code","channel"))
    header_set = True

   #os.path.expanduser('~') + '/report_file.csv'
  with open(log_location + "/" + 'reports/glo-ssl-requests_' + channel + '.csv', mode='a+') as report_file :
    writer = csv.writer(report_file)
    writer.writerows(logList)
    report_file.close()
    print("Report generated")


def backupLogFile(file):
  #subprocess.call(["mv", log_location + "/" + file, backup_location + "/" + file])
  shutil.move(log_location + "/" + file, backup_location + "/" + file)
  print("File backup completed")



if __name__ == "__main__":
  print("The web request log processor app is now launched...")

  props = getAppProperties("app.properties", "=")
  #print(props)

  channel = props.get("channel")
  log_location = props.get("log_location")
  backup_location = props.get("backup_location")  
  regex = props.get("ssl_log_regex")
  
  error_log_regex = props.get("error_regex")
  
  loadLogs()
