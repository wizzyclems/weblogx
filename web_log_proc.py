#!/usr/bin/env python3

import time
import re
import csv
import os
from datetime import datetime
from util.util import getAppProperties
from util.util import backupLogFile
from util.util import deleteBackedupItems
from entity.LogLine import LogLine

from db.oracle_db import createOracleDBConnection
from db.oracle_db import writeManySSLLogs



log_location = "logs"
backup_location = "logs/backup"
connection = None
matchedRowCount = 0
#regex_v1 = r'\[([\d]{1,2}/[\w]{3,3}/[\d]{2,4}):([\d]{1,3}:[\d]{1,3}).*]\s([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\s([\w\d\.\-]*)\s([A-Z\d\-]*)\s\"([A-Z]{0,4})\s?([\w\d/\-\.]*)\s?([\w\d/\-\.]*)\"\s?([\d\-]*)\s?([\w\.]*)\s?([\d\-]*)\s?([\w\d/\-\.:]*)'
regex = r'\[([\d]{1,2}/[\w]{3,3}/[\d]{2,4}):([\d]{1,3}:[\d]{1,3}).*]\s([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\s([\w\d\.\-]*)\s([A-Z\d\-]*)\s\"([a-zA-Z]{0,})\s?([^ ]*)\s?([\w\d/\-\.]*)\"\s?([\d\-]*)\s?([\w\.]*)\s?([\d\-]*)\s?([\w\d/\-\.:]*)'
error_log_regex = r'^(\d{4}/\d{1,2}/\d{1,2}) (\d{1,2}:\d{1,2}).*client: ([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}).*request: \"([A-Z]+) ([/\w-]+).*upstream: \"[a-z:/]*([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}):(\d{4})'
header_set = False

fileCache = ""
unMatchedLine = ""

db_user = ""
db_password = ""
db_host = ""
db_name = ""
db_port = "" 

dbConnection = None


def getDBConnection():
  global dbConnection

  if dbConnection == None :
    print("Connecting to the database server...")
    dbConnection = createOracleDBConnection(db_name,db_password, db_host)
    print("Database connection successful...")
  
  return dbConnection


def read_SSL_Log(file, channel, webServer, logType):
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
        markUnmatchLogLine(line)
        continue

      if len(result.groups()) < 12 :
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
      logLine.setCreateDate(datetime.now())
      logLine.setRequestDate(result.group(1))
      logLine.setRequestTime(result.group(2))
      logLine.setSourceServer(result.group(3))
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
      logLine.setWebServer(webServer)
      logLine.setLogType(logType)

      logEntry = [ logLine.getCreateDate(),logLine.getRequestDate(),logLine.getRequestTime(),
        logLine.getRequestMethod(),logLine.getRequest(),logLine.getSourceServer(),logLine.getSecurityProtocol(),
        logLine.getCypherSuite(),logLine.getHttpVersion(), logLine.getRequestSize(),logLine.getRequestHost(),
        logLine.getResponseStatusCode(), logLine.getResponseServer(),logLine.getChannel(),logLine.getLogType(),
        logLine.getWebServer()]

      logList.append( logEntry )

      matchedRowCount = matchedRowCount + 1
      
    log.close()

  print("The file row count is {}".format(fileRowCount))
  print("The matched row count is {}".format(matchedRowCount))

  return logList


def deleteBackups():

  try:

    if os.path.exists(log_location) and os.path.isdir(log_location):
      log_files = os.listdir(log_location) 
    else:
        print("The specified log location either does not exist or is not a folder. Kindly confirm and run the application again.")
        return

  except(OSError ):
    print("Error encountered while trying to read from the log location. Kindly confirm the log location path is correct and try again.")
    print("Deletion of backed up files will be terminated. Application processing will continue now...")
    return
  
  for server_log in log_files:
    #delete log backups for each server...
    deleteBackedupItems( os.path.join(log_location,server_log,"backup") )

  print("Backed up items for all servers have now been cleaned up...")


def loadLogs():

  try:

    if os.path.exists(log_location) and os.path.isdir(log_location):
      log_files = os.listdir(log_location) 
    else:
        print("The specified log location either does not exist or is not a folder. Kindly confirm and run the application again.")
        exit()

  except(OSError ):
    print("Error encountered while trying to read from the log location. Kindly confirm the log location path is correct and try again.")
    print("Terminating the application now...")
    exit()
  
  for server_log in log_files:
    channel = ''

    if not os.path.isdir(log_location + "/" + server_log) :
      print("{} is not a directory. Item will be skipped.".format(server_log))
      continue

    if not (server_log.startswith("172") or server_log.startswith("10")) :
      print("{} does not start with known folder name. Item will be skipped.".format(server_log))
      continue


    if server_log.startswith("172") :
      channel = "DMZ"

    if server_log.startswith("10") :
      channel = "LAN"

    webServer = server_log
    print("The web server IP is {}".format(webServer))
    log_folder = log_location + "/" + server_log
    print("The log folder path is {}".format(log_folder))
    print("The channel is {}".format(channel))
    print("attempting to process server log now...")
    processSpecificServerLogs(channel, webServer, log_folder)


def processSpecificServerLogs(channel, webServer,log_folder):
  

  try:
    if os.path.exists(log_folder) and os.path.isdir(log_folder):
      log_files = os.listdir(log_folder) 
    else:
        print("The specified log folder either does not exist or is not a folder. Kindly confirm and run the application again.")
        exit()
  
  except(OSError ):
    print("Error encountered while trying to read from the log location. Kindly confirm the log location path is correct and try again.")
    print("Terminating the application now...")
    exit()

  for log in log_files:
    
    if not os.path.isfile(log_folder + '/' + log):
      print("The specified item '{}' is not a file. Item will be skipped.".format(log))
      continue

    # skip the file if it is not an ssl or ssl-error log file.
    if not ( ("ssl" in log) or ("ssl-error" in log) ):
       print("{} is not a supported log file type. Item will be skipped.".format(log))
       continue

    if hasLogBeenProcessed( log_folder + "/" + log ) :
      backupLogFile(log_folder + "/" + "backup", log_folder + "/" + log)
      continue

    # skip the log file if it is zipped.
    #TODO I think it would be useful to implement reading of zipped log files
    if ".gz" in log :
      print("Zipped files are not yet supported. {}".format(log))
      continue

    # Read and process ssl logs
    if "ssl" in log :
      #reading successful SSL logs
      print("SSL log found {}".format(log))
      logType = "SSL"
      logList = read_SSL_Log(log_folder + "/" + log, channel, webServer, logType)

      #below line inserts each log entry into an Oracle database
      writeManySSLLogs( getDBConnection(), logList)

      #put the item in the file cache to mark it has processed
      putInFileCache(log_folder + "/" + log)
      print("File processing done.")
      #generateReport(logList)
      #print("Row count for file {} is {}".format(log_location + "/" + log, rowCount))

    # Read and process ssl-error logs. 
    # TODO add implementation for processing ssl-error logs
    if "ssl-error.log" in log :
      #reading successful SSL logs
      print("No suppport yet for reading SSL error log files")
      logType = "SSL-ERROR"
      continue      

      #below line backs up the logfilethat was processed
    
    # Once reading and processing logs are complete, backup the log file in the specified location.
    backupLogFile(log_folder + "/" + "backup", log_folder + "/" + log)
    

def hasLogBeenProcessed(log_file) :
  global fileCache

  if not os.path.isfile(log_file):
    print("The specified item '{}' is not a file. Item will be skipped.".format(log_file))
    return True
  
  processed = itemInFileCache(log_file)

  if processed :
    print("{} has already been processed. Log will be skipped.".format(log_file))
  else:
    print("{} has not been processed yet.".format(log_file))
      
  return processed


def itemInFileCache(cache_item):
  global fileCache

  with open(fileCache, mode='a+') as cache:
    inCache = False
    cache.seek(0)
    for line in cache.readlines():
      if cache_item in line :
        inCache = True
        break

    return inCache


def putInFileCache(cache_item):
  global fileCache

  with open(fileCache, mode='a+') as cache:
    cache.write(cache_item + "\n")


def markUnmatchLogLine(unMatchedLogLine) :
  global unMatchedLine
  
  with open(unMatchedLine, mode='a+') as file:
    file.write(unMatchedLogLine)


def generateReport(logList):
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






if __name__ == "__main__":
  print("The web request log processor app is now launched...")

  props = getAppProperties("app.properties", "=")
  #print(props)

  #channel = props.get("channel")
  log_location = props.get("log_location")
  backup_location = props.get("backup_location")  
  regex = props.get("ssl_log_regex")
  #webServer = props.get("web_server")
  

  fileCache = props.get("file_cache")
  unMatchedLine = props.get("unmatched-logline")

  error_log_regex = props.get("error_regex")

  db_user = props.get("db_user")
  db_password = props.get("db_password")
  db_host = props.get("db_host")
  db_name = props.get("db_name")
  db_port = props.get("db_port")

  while True :
    loadLogs()
    print("All logs are now processed. The application will sleep now.")
    time.sleep(20)
    deleteBackups()
    print("===================================================================")
    print("=================== Fresh Start of processing... ==================")

#if __name__ == "__main__":
    #test_list = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60]

    #for i in chunker(test_list, 11) :
        #print(i)