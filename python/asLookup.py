import subprocess


# Uses AS Path Tool by Haseeb Niaz @ Networking Research Group, Stony Brook University
# more info mniaz@cs.stonybrook.edu

# Compose a query to haseeb's AS lookup service
# echo "[command]" | netcat as.haseebniaz.com 22
# -info	Get info about an AS, IP or IP prefix
# 				-> echo "-info ASNUM"


class asLookup:

    def sendQuery(self, query):
        lookupServer = 'as.haseebniaz.com'
        lookupServerPort = '22'

        # open echo process and pipe its output
        echoProcess = subprocess.Popen(("echo", query), stdout=subprocess.PIPE)

        # pipe in echoProcess's output into netcat, capture result into buffer
        lookupOutput = subprocess.check_output(("netcat", lookupServer, lookupServerPort), stdin=echoProcess.stdout)

        # decode output buffer as UTF-8 string
        lookupResultString = lookupOutput.decode("UTF-8")

        return lookupResultString

    def asLookup(self, inputAS):

        inputQuery = "-info "+inputAS
        reply = self.sendQuery(inputQuery)

        resultParse = [x.strip() for x in reply.split('|')]

        self.asNumber = inputAS
        self.country = resultParse[5]
        self.registry = resultParse[6]
        self.asAllocated = resultParse[7]
        self.asName = resultParse[8]
        return

    def ipLookup(self, inputIP):

        inputQuery = "-info "+inputIP
        reply = self.sendQuery(inputQuery)

        resultParse = [x.strip() for x in reply.split('\n')]

        resultLine = resultParse[1] # first line is headers, discard
        resultLine = [x.strip() for x in resultLine.split('|')]


        self.asNumber = resultLine[1]
        self.ipAddr = inputIP
        self.bgpPrefix = resultLine[2]
        self.country = resultLine[3]
        self.registry = resultLine[4]
        self.allocated = resultLine[5]
        self.asName = resultLine[6]

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
print("name=", asLookup('AS12', 1).asName)
print("asNumber=", asLookup('AS12', 1).asNumber)
print("asRegistry=", asLookup('AS12', 1).registry)
print("asCountry=", asLookup('AS12', 1).country)

result = asLookup('129.49.115.147', 2)

# Print which keys/instance variables are present
print(result.__dict__.keys())

print('AS NAME = ', result.asName)
'''



