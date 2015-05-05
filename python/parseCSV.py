import csv
import geoip2.database
import numpy as np

from IPy import IP
from asLookup import asLookup
from os.path import expanduser
home = expanduser("~")

geoDB = geoip2.database.Reader(home+'/cse534/GeoLite2-City.mmdb')



class geoIP:
    def __init__(self, ipAddr):
        try:
            response = geoDB.city(ipAddr)
            self.country = response.country.name
            self.continent = response.continent.names['en']
        #except geoip2.errors.AddressNotFoundError:
        except:
            self.country = "null"
            self.continent = "null"

class hopInfo:
    def __init__(self, rtt_1, rtt_2, rtt_3):
        # print("hopInfo:", rtt_1, rtt_2, rtt_3)

        hopRTT1 = [x.strip() for x in rtt_1.split(',')]
        hopRTT1[1] = hopRTT1[1][4:]
        self.hopRTT1 = hopRTT1[1]

        hopRTT2 = [x.strip() for x in rtt_2.split(',')]
        hopRTT2[1] = hopRTT2[1][4:]
        self.hopRTT2 = hopRTT1[1]

        hopRTT3 = [x.strip() for x in rtt_3.split(',')]
        hopRTT3[1] = hopRTT3[1][4:]
        self.hopRTT3 = hopRTT1[1]

        self.hopAddr = hopRTT1[0]

        # print( 'hopRTT[1]=',hopRTT1[1]  )

        print("Mean",np.mean([float(hopRTT1[1]), float(hopRTT2[1]), float(hopRTT3[1])]))


        '''
        print("hopAddr:",self.hopAddr)
        print("hopRTT1:",self.hopRTT1)
        print("hopRTT2:",self.hopRTT2)
        print("hopRTT3:",self.hopRTT3)
        '''

class traceRt:

    def checkCase1(self):
        #############################
        #       CASE No. 1
        # Check if src & dst are in same country and one of the hops is in a different country
        ############################
        circuitousness = 0
        if self.srcGeo.country == self.dstGeo.country:
            print("Hello Case1!")
            for each in self.hopListGeo:
                print("Hop:", each.country, each.continent)
            for each in self.hopListGeo:
                if each.country != self.srcGeo.country and each.country != "null":
                    print("Circuit Case1 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase1(self):
        # TODO: fill in analyzeCase1
        # Case 1: Src and Dst are in the same country, intermediate hop is outside ctry
        print("Analyze Case 1:\n Source and Destination are in ", self.srcGeo.country)


    def checkCase2(self):
        ##########################
        #       CASE No. 2
        # Check if src & dst are in the same continent and one of the hops is in a different continent
        ##########################
        circuitousness = 0
        if self.srcGeo.continent == self.dstGeo.continent:
            print("Hello Case2!")
            for each in self.hopListGeo:
                print("Hop:", each.country, each.continent)
            for each in self.hopListGeo:
                if each.continent != self.srcGeo.continent and each.continent != "null":
                    print("Circuit Case2 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase2(self):
        # Case 1: Src and Dst are in the same continent, intermediate hop is outside continent
        print("Analyze Case 2: Src and Dst are both in the same continent -", self.srcGeo.continent)



    def checkCase3(self):
        #############################
        #       CASE No. 3
        # Check if src & dst are in continents A & B and one of the hops is in a continent C such that C != A && C != B
        ############################
        circuitousness = 0
        if self.srcGeo.continent != self.dstGeo.continent:
            print("Hello Case3!")
            for each in self.hopListGeo:
                print("Hop:", each.country, each.continent)
            for each in self.hopListGeo:
                if each.continent != self.srcGeo.continent and each.continent != self.dstGeo.continent and each.continent != "null":
                    print("Circuit Case3 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase3(self):
        # TODO: fill in analyzeCase3
        # Case 1: Src and Dst are in the same continent, intermediate hop is outside continent
        print("Analyze Case 3")

    def csvWrite(self, row, path):
        writer = csv.writer(path)
        writer.writerow(row)
        return

    def __init__(self, csvRow, case1filePath, case2filePath, case3filePath):
        self.csvRow = csvRow
        print("csvline = ",self.csvRow)
        self.dstIP = self.csvRow[0]
        self.srcIP = self.csvRow[1]

        self.hopList = []

        print("length of csvRow=",len(self.csvRow))
        for i in range(2, len(self.csvRow)-2, 3):
            hop = hopInfo(self.csvRow[i], self.csvRow[i+1], self.csvRow[i+2])
            self.hopList.append(hop)

        isError = 0

        # check for error in hop RTTs, skip processing if there are.
        for hop in self.hopList:
            try:
                print("Mean:", np.mean([float(hop.hopRTT1[1]), float(hop.hopRTT2[1]), float(hop.hopRTT3[1])]))
            except:
                isError = 1

        if isError == 0:

            # get GEO ip on src, dst, and hops
            self.dstGeo = geoIP(self.dstIP)
            self.srcGeo = geoIP(self.srcIP)

            self.hopListGeo = []
            for hop in self.hopList:
                self.hopListGeo.append(geoIP(hop.hopAddr))

            self.hopListAS = []
            for hop in self.hopList:
                asResult = asLookup(hop.hopAddr, 2)
                self.hopListAS.append(asLookup(hop.hopAddr, 2))

                print('AS Number =', self.hopListAS[-1].asNumber)


            print(self.hopListAS[:])

            print("------INFO------")
            print("Source:", self.srcGeo.country, self.srcGeo.continent)
            print("Destination:", self.dstGeo.country, self.dstGeo.continent)

            # Check our three cases of circuitousness:
            case1status = self.checkCase1()
            if case1status == 1:
                self.analyzeCase1()
                self.csvWrite(csvRow, case1filePath)
                # csvwrite csvRow here

            case2status = self.checkCase2()
            if case2status == 1:
                self.analyzeCase2()
                self.csvWrite(csvRow, case2filePath)

            case3status = self.checkCase3()
            if case3status == 1:
                self.analyzeCase3()
                self.csvWrite(csvRow, case3filePath)

            print("------END-----")

csvFilePath = open(home+'/cse534/data/content_traceroute/1766609.csv')

# output instances of case1/2/3 to csv:-
case1filePath = open(home+'/cse534/output/case1/case1.csv', 'r+')
case2filePath = open(home+'/cse534/output/case2/case2.csv', 'r+')
case3filePath = open(home+'/cse534/output/case3/case3.csv', 'r+')

csvFile = csv.reader(csvFilePath, delimiter=';')

for row in csvFile:
    result = traceRt(row, case1filePath, case2filePath, case3filePath)
    print("------------------------------- Next Row -------------------------------")

case1filePath.close()
case2filePath.close()
case3filePath.close()