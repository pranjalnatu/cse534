import subprocess
from IPy import IP


# Revised asLookup.py tool to use Team CYMRU's IP to AS mapping for stability
# seems to be the same (or similar implementation) as Haseeb's AS Path tool
# http://www.team-cymru.org/IP-ASN-mapping.html


class asLookup:

    def sendQuery(self, query, type):
        if type == 1: #asLookup
            lookupServer = "asn.cymru.com"
            lookupServer = query+"."+lookupServer
            lookupSuccess = 0
            try:
                lookupOutput = subprocess.check_output(("dig", "+short", lookupServer, "TXT"))
                lookupSuccess = 1
            except:
                lookupOutput = "null"

        elif type == 2: #ipLookup
            lookupServer = "origin.asn.cymru.com"

            # add ASnumber into server address, need to reverse the octets
            ipParse = [x.strip() for x in query.split('.')]
            ipReverse = ipParse[::-1]
            ipReverseString = ".".join(ipReverse)

            # join reversed IP string with the lookup server
            lookupServer = ipReverseString+"."+lookupServer

            lookupSuccess = 0
            try:
                lookupOutput = subprocess.check_output(("dig", "+short", lookupServer, "TXT"))
                lookupSuccess = 1
            except:
                lookupOutput = "null"

        if lookupSuccess == 1:
            lookupResultString = lookupOutput.decode("UTF-8")
            lookupResultString = lookupResultString.replace("\"", "")
        else:
            lookupResultString = "null"
        # print(lookupResultString)
        return lookupResultString

    def asLookup(self, inputAS):

        inputQuery = inputAS
        reply = self.sendQuery(inputQuery, 1)

        resultParse = [x.strip() for x in reply.split('|')]

        if len(resultParse) <=1 :
            self.asLookupSucceed = 0
        else:
            self.asLookupSucceed = 1
            self.asNumber = inputAS
            self.country = resultParse[1]
            self.registry = resultParse[2]
            self.asName = resultParse[4]

        return

    def ipLookup(self, inputIP):
        self.ipAddr = inputIP

        inputQuery = inputIP
        reply = self.sendQuery(inputQuery, 2)

        resultParse = [x.strip() for x in reply.split('\n')]

        resultLine = resultParse[0]
        resultLine = [x.strip() for x in resultLine.split('|')]

        if len(resultLine) <= 1:
            self.ipToASLookupSucceed = 0
        else:
            self.ipToASLookupSucceed = 1

        privateCheck = IP(inputIP)
        if privateCheck.iptype() != 'PRIVATE' and self.ipToASLookupSucceed == 1:
            # print(inputIP)
            # print(resultLine)
            self.isPrivate = False
            self.asNumber = resultLine[0]
            self.bgpPrefix = resultLine[1]
            self.country = resultLine[2]
            self.registry = resultLine[3]
            self.allocationDate = resultLine[4]
            self.asLookup('AS'+self.asNumber)
        else:
            self.isPrivate = True

    def __init__(self, inputString, lookupType):

        # lookupType 1: look up an AS number
        # lookupType 2: look up an IP address

        if lookupType == 1:
            self.asLookup(inputString)
        elif lookupType == 2:
            self.ipLookup(inputString)
        else:
            print("Lookup type not supported")
        return


'''
# SAMPLE USAGE
print("-----Querying for AS12-----")
sampleASnumber = 'AS12'

result = asLookup(sampleASnumber,1)
# Print which keys/instance variables are present
print("keys available:", result.__dict__.keys())
print("name=", result.asName)
print("asNumber=", result.asNumber)
print("asRegistry=", result.registry)
print("asCountry=", result.country)


print("-----Querying for IP 129.49.115.147")
result = asLookup('129.49.115.147', 2)

# Print which keys/instance variables are present
print("keys available:", result.__dict__.keys())
print("items:", result.__dict__.items())


print("-----Querying for IP 192.168.1.1")
result = asLookup('192.168.1.1', 2)

# Print which keys/instance variables are present
print("keys available:", result.__dict__.keys())
print("items:", result.__dict__.items())

'''
