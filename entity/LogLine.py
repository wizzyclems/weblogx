

class LogLine:
    requestDate = ''
    requestTime = ''
    sourceIp = ''
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


    def __init__(self):
        self.requestDate = ''
        self.requestTime = ''
        self.sourceIp = ''
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

    def getRequestDate(self):
        return self.requestDate

    def setRequestDate(self,requestDate):
        self.requestDate = requestDate

    def getRequestTime(self):
        return self.requestTime

    def setRequestTime(self,requestTime):
        self.requestTime = requestTime
    
    def getSourceIp(self):
        return self.sourceIp

    def setSourceIp(self,sourceIp):
        self.sourceIp = sourceIp

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

    def __str__(self):
        return self.getLogDate() + ',' + self.getLogTime() + ',' + self.getSourceIp() + ',' + self.getSecurityProtocol() + ',' + self.getCypherSuite() + ',' + self.getRequestMethod() + ',' + self.getRequest() + ',' + self.getHttpVersion() + ',' + self.getRequestSize()  + ',' + self.getRequestHost() + ',' + self.getResponseStatusCode()  + ',' + self.getResponseServer() + ',' + self.getChannel()

    