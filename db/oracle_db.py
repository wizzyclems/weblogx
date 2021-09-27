#!/usr/bin/env python3

import cx_Oracle
from datetime import datetime
import traceback
from util.util import chunker

dbCursor = None
dbConnection = None
batchSize = 10000

# Below function establishes connection with the database
def createOracleDBConnection(db_name,db_password, db_host):
    # Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
    print("attempting connection to the database...")
    dbConnection = cx_Oracle.connect(db_name, db_password, db_host)
    print("Connection to database successful...")
    return dbConnection


def getDBCursor():
  global dbCursor

  if dbCursor == None :
    print("Retrieving database connection cursor...")
    dbCursor = dbConnection.cursor()
    print("Database cursor successfully retrieved....")
  
  return dbCursor
  #return createPostgresDBConnection()


# Below function retrieves SSL logs from the database.
def get_SSL_Log(dbCursor, param):

    try:
        dbCursor.execute("""
                SELECT msisdn, unique_id,create_date, activationstatusenum FROM bfp_sync_log
                WHERE msisdn = :msisdn""",msisdn = '08030491762')
        
        for msisdn, unique_id,create_date, activation_status in dbCursor:
            print("Values:", msisdn, unique_id,create_date, activation_status)

    except:
        # Rollback in case there is any error
        traceback.print_exc()
        dbCursor.rollback()
        
def writeManySSLLogs2(dbCursor, logList):
    
    sql = """INSERT INTO web_server_ssl_logs(source_ip,destination_ip,destination_port,
        request_date,request_time,request_method,request,request_size)
        VALUES ( :createDate, :reqDate, :reqHour, :reqMethod, :req , :sourceServer)"""
    try:
        dbCursor.executemany(sql, logList)
        dbCursor.commit()
        print("Logs successfully written to the database and committed...")
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        traceback.print_exc()
        dbCursor.rollback()


def writeManySSLLogs(dbConnection, logList):
    global batchSize

    sql = """INSERT INTO web_server_ssl_logs(create_date, request_date, request_time,
        request_method, request, source_server,SECURITY_PROTOCOL,CIPHERSUITE,
        HTTP_VERSION,REQUEST_SIZE,REQUEST_HOST,STATUS_CODE,RESPONSE_SERVER,CHANNEL,LOGTYPE, web_server)
        VALUES ( :createDate, :reqDate, :reqTime, :reqMethod, :req , :sourceServer, :secProtocol, :cipherSuite,
        :httpVersion, :reqSize, :reqHost, :statusCode, :respServer, :channel, :logType, :webServer)"""
    try:
        dbCursor = dbConnection.cursor()
        for data in chunker(logList, batchSize) :
            dbCursor.executemany(sql, data)
            print(dbCursor.rowcount, "rows inserted")
            dbConnection.commit()

        print("logs successfully persisted to the database...")

    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        traceback.print_exc()
        dbConnection.rollback()


def writeManyErrorLogs(connection, logList):
    
    sql = """INSERT INTO web_server_error_logs(create_date, root_cause, error_message,
         request_date, source_ip)
        VALUES ( :createDate, :rootCause, :errorMessage, :reqDate, :sourceIP)"""
    try:
        connection.cursor().executemany(sql, logList)
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        connection.rollback()


# Below function writes SSL logs from the database.
def write_SSL_Log(connection, param):
    # Prepare SQL query to INSERT a record into the database.
    "insert into MyTable values (:idbv, :nmbv)", [1, "Fredico"]
    sql = "INSERT INTO web_server_ssl_logs(create_date, request_date, request_hour, \
        request_method, request, source_server) \
        VALUES ( :createDate, :reqDate, :reqHour, :reqMethod, :req , :sourceServer)"
    try:
        connection.cursor().execute(sql, [ datetime.today(), param[0], param[1], param[2], param[3], param[4]])
        connection.commit()
    except:
        # Rollback in case there is any error
        print("Error while writing to the database")
        traceback.print_exc()
        connection.rollback()

def commitOperation(connection):
    connection.commit()

def closeDBConnection(connection):
    connection.close()


#cx_Oracle.init_oracle_client(lib_dir="/Applications/oracle/instantclient_19_8")

