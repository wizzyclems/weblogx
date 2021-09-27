



#Goals
- Read from properties file - Done
- Ensure that the app can read both unix and windows path from the properties files - Done
- Implement exception handling while reading from the log location path - Done
- Implement regular expression for reading from ssl request log files - Done
- The log location specified in the properties file is expected to be a folder that contains folders named according to the web server the log is from.
- DMZ server folders are expected to start with 172, while LAN servers are expected to start with 10
- The above item is how the application determines the channel of the traffic. Whether it is LAN or DMZ
- processed log files are backed up in a backup folder inside the web server IP log folder

- Implement regular expression for reading from access log files
- Implement regular expression for reading from error log files
- spawn multiple threads to read from each web server location
