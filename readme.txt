



#Goals
- Read from properties file - Done
- Ensure that the app can read both unix and windows path from the properties files - Done
- Implement exception handling while reading from the log location path - Done
- Implement regular expression for reading from ssl request log files - Done
- The log location specified in the properties file is expected to be a folder that contains folders named according to the web server the log is from. - Done
- DMZ server folders are expected to start with 172, while LAN servers are expected to start with 10 - Done
- The above item is how the application determines the channel of the traffic. Whether it is LAN or DMZ - Done
- processed log files are backed up in a backup folder inside the web server IP log folder - Done

Done
- Implement deletion of backed up log files with a new function
- Store the IP of the web server the log files are extracted from.


In Progress
- 


TODO
- Push logs from all the servers to the processor location
- run the migrator to process the new logs for october
- configure a windows task schedule to migrate the logs every morning by 2am.

- implement a scheduler for the migrator app to run on linux server
- Implement a process to delete backed up log files when the app is sleeping.
- Implement regular expression for reading from access log files
- Implement regular expression for reading from error log files
- spawn multiple threads to read from each web server location
- Implement application logging 



log_location=/data/fix/sw/web_server_logs
backup_location=/Users/iudoh/wizzyapps/web_server_logs_processor/backup

file_cache=/data/fix/sw/apps/weblogx/cache.txt
unmatched-logline=/data/fix/sw/apps/weblogx/unmatchedline.txt