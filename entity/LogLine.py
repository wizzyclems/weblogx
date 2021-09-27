

class LogLine:
    requestDate = ''
    requestTime = ''
    sourceServer = ''
    securityProtocol = ''
    cipherSuite = ''
    requestMethod = ''
    request = ''
    httpVersion = ''
    requestSize = ''
    requestHost = ''
    responseStatusCode = ''
    responseServer = ''
    channel = ''
    webServer = ''
    logType = ''
    createDate = ''

    def __init__(self):
        self.requestDate = ''
        self.requestTime = ''
        self.sourceServer = ''
        self.securityProtocol = ''
        self.cipherSuite = ''
        self.requestMethod = ''
        self.request = ''
        self.httpVersion = ''
        self.requestSize = ''
        self.requestHost = ''
        self.responseStatusCode = ''
        self.responseServer = ''
        self.channel = ''
        self.webServer = ''
        self.logType = ''
        self.createDate = ''

    def getCreateDate(self):
        return self.createDate

    def setCreateDate(self,createDate):
        self.createDate = createDate

    def getRequestDate(self):
        return self.requestDate

    def setRequestDate(self,requestDate):
        self.requestDate = requestDate

    def getRequestTime(self):
        return self.requestTime

    def setRequestTime(self,requestTime):
        self.requestTime = requestTime
    
    def getSourceServer(self):
        return self.sourceServer

    def setSourceServer(self,sourceServer):
        self.sourceServer = sourceServer

    def getSecurityProtocol(self):
        return self.securityProtocol

    def setSecurityProtocol(self,securityProtocol):
        self.securityProtocol = securityProtocol

    def getCypherSuite(self):
        return self.cypherSuite

    def setCypherSuite(self,cypherSuite):
        self.cypherSuite = cypherSuite

    def getRequestMethod(self):
        return self.requestMethod

    def setRequestMethod(self,requestMethod):
        self.requestMethod = requestMethod

    def getRequest(self):
        return self.request

    def setRequest(self,request):
        self.request = request

    def getHttpVersion(self):
        return self.httpVersion

    def setHttpVersion(self,httpVersion):
        self.httpVersion = httpVersion

    def getRequestSize(self):
        return self.requestSize

    def setRequestSize(self,requestSize):
        self.requestSize = requestSize

    def getRequestHost(self):
        return self.requestHost

    def setRequestHost(self,requestHost):
        self.requestHost = requestHost

    def getResponseStatusCode(self):
        return self.responseStatusCode

    def setResponseStatusCode(self,responseStatusCode):
        self.responseStatusCode = responseStatusCode

    def getResponseServer(self):
        return self.responseServer

    def setResponseServer(self,responseServer):
        self.responseServer = responseServer

    def getChannel(self):
        return self.channel

    def setChannel(self,channel):
        self.channel = channel

    def getWebServer(self):
        return self.webServer

    def setWebServer(self,webServer):
        self.webServer = webServer

    def getLogType(self):
        return self.logType

    def setLogType(self,logType):
        self.logType = logType

    def __str__(self):
        return self.getCreateDate() + ',' + self.getRequestDate() + ',' + self.getRequestTime() + ',' + self.getRequestMethod()  + ',' + self.getRequest() + ',' + self.getSourceServer() + ',' + self.getWebServer() + ',' + self.getSecurityProtocol() + ',' + self.getCypherSuite()  + ',' + self.getHttpVersion() + ',' + self.getRequestSize()  + ',' + self.getRequestHost() + ',' + self.getResponseStatusCode()  + ',' + self.getResponseServer() + ',' + self.getChannel() + ',' + self.getLogType() 
        

        


    