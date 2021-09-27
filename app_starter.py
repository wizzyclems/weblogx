#!/usr/bin/env python


from util import getAppProperties
from web_log_proc import startProcessing

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

db_user = ""
db_password = ""
db_host = ""
db_name = ""
db_port = "" 



if __name__ == "__main__":
  print("The web request log processor app is now launched...")

  props = getAppProperties("app.properties", "=")
  #print(props)

  channel = props.get("channel")
  log_location = props.get("log_location")
  backup_location = props.get("backup_location")  
  regex = props.get("ssl_log_regex")
  
  error_log_regex = props.get("error_regex")

  db_user = props.get("db_user")
  db_password = props.get("db_password")
  db_host = props.get("db_host")
  db_name = props.get("db_name")
  db_port = props.get("db_port")

  
  startProcessing()
