import csv
import geoip2.database
import numpy as np
import time

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
        self.hopRTT2 = hopRTT2[1]

        hopRTT3 = [x.strip() for x in rtt_3.split(',')]
        hopRTT3[1] = hopRTT3[1][4:]
        self.hopRTT3 = hopRTT3[1]

        self.hopAddr = hopRTT1[0]

        # check if all the IPs in the hop match
        # if they don't, there is an error - each hop should have 3 RTTs and we've parsed incorrectly
        if (hopRTT1[0] == hopRTT2[0]) and (hopRTT1[0] == hopRTT3[0]):
            self.isError = 0
        else:
            self.isError = 1

        # Calculate the mean RTT for this hop
        if self.isError == 0:
            try:
                self.hopMean = np.mean([float(hopRTT1[1]), float(hopRTT2[1]), float(hopRTT3[1])])
            except:
                self.isError == 1


class traceRt:

    def checkCase1(self):
        #############################
        #       CASE No. 1
        # Check if src & dst are in same country and one of the hops is in a different country
        ############################
        circuitousness = 0
        if self.srcGeo.country == self.dstGeo.country:
            for each in self.hopListGeo:
                if each.country != self.srcGeo.country and each.country != "null":
                    print("Circuit Case1 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase1(self):
        # Case 1: (src, dest) in same country, (one or more hops) in different country
        print("**** Analyze Case 1: ****")
        # get source and destination continent
        print("Source country:", self.srcGeo.country)
        print("Destination country:", self.dstGeo.country)


        itemInd = 0
        for item in self.hopListGeo:
            print('Hop #', itemInd, ':', self.hopList[itemInd].hopAddr, "-", self.hopListGeo[itemInd].country, ",", self.hopListGeo[itemInd].continent)
            if item.country!="null" and (item.country != self.srcGeo.country) and (item.country != self.dstGeo.country):
                print('Hop #', itemInd, '---- case 1 hop ----')
                # check RTT difference between this hop and the one before it
                if self.hopList[itemInd].isError == 0 and self.hopList[itemInd-1].isError == 0:
                    if hasattr(self.hopList[itemInd], 'hopMean') and hasattr(self.hopList[itemInd-1], 'hopMean'):
                        hopDiff = self.hopList[itemInd].hopMean - self.hopList[itemInd-1].hopMean
                        print('Hop mean RTT:', self.hopList[itemInd].hopMean)
                        print('Delta RTT =', hopDiff)

                    else:
                        print('Could not calculate delta RTT')

                else:
                    print('Could not calculate delta RTT')

                print('This hop is not in the src/dst country:', item.country)
                print('Hop IP:', self.hopListAS[itemInd].ipAddr)

                if self.hopListAS[itemInd].ipToASLookupSucceed == 1:
                    print('Hop AS#:', self.hopListAS[itemInd].asNumber)
                    print('Hop Country (from AS lookup):', self.hopListAS[itemInd].country)
                else:
                    print('Hop AS info - country and AS# unsuccessful for this hop!')

                print('Hop Country (from GeoIP lookup):', item.country)
            itemInd = itemInd+1

    def checkCase2(self):
        ##########################
        #       CASE No. 2
        # Check if src & dst are in the same continent and one of the hops is in a different continent
        ##########################
        circuitousness = 0
        if self.srcGeo.continent == self.dstGeo.continent:
            for each in self.hopListGeo:
                if each.continent != self.srcGeo.continent and each.continent != "null":
                    print("Circuit Case2 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase2(self):
        # Case 2: (src, dest) in SAME continent, (one or more hops) in different continent
        print("**** Analyze Case 2: ****")
        caseError = 0
        # get source and destination country
        print("Source continent:", self.srcGeo.continent)
        print("Destination continent:", self.dstGeo.continent)
        if self.srcGeo.continent == self.dstGeo.continent:
            print("Source and Destination continent match!")
        else:
            caseError = 1


        itemInd = 0
        for item in self.hopListGeo:
            print('Hop #', itemInd, ':', self.hopList[itemInd].hopAddr, "-", self.hopListGeo[itemInd].country, ",", self.hopListGeo[itemInd].continent)
            if item.continent!="null" and (item.continent != self.srcGeo.continent) and (item.continent != self.dstGeo.continent):
                print('Hop #', itemInd, '---- case 2 hop ----')
                # check RTT difference between this hop and the one before it
                if self.hopList[itemInd].isError == 0 and self.hopList[itemInd-1].isError == 0:
                    if hasattr(self.hopList[itemInd], 'hopMean') and hasattr(self.hopList[itemInd-1], 'hopMean'):
                        hopDiff = self.hopList[itemInd].hopMean - self.hopList[itemInd-1].hopMean
                        print('Hop mean RTT:', self.hopList[itemInd].hopMean)
                        print('Delta RTT =', hopDiff)
                        hopThreshold = 80
                        if hopDiff >= 80:
                            print('Delta RTT is above threshold')
                        else:
                            print('DeltaRTT is below threshold, likely a false positive result')

                    else:
                        print('Could not calculate delta RTT')

                else:
                    print('Could not calculate delta RTT')

                print('This hop is neither in the src nor  in the dst continent:', item.continent)
                print('Hop IP:', self.hopListAS[itemInd].ipAddr)

                if self.hopListAS[itemInd].ipToASLookupSucceed == 1:
                    print('Hop AS#:', self.hopListAS[itemInd].asNumber)
                    print('Hop Country (from AS lookup):', self.hopListAS[itemInd].country)
                else:
                    print('Hop AS info - country and AS# unsuccessful for this hop!')

                print('Hop Country (from GeoIP lookup):', item.country)
            itemInd = itemInd+1


    def checkCase3(self):
        #############################
        #       CASE No. 3
        # Check if src & dst are in continents A & B and one of the hops is in a continent C such that C != A && C != B
        ############################
        circuitousness = 0
        if self.srcGeo.continent != self.dstGeo.continent:
            for each in self.hopListGeo:
                if each.continent != self.srcGeo.continent and each.continent != self.dstGeo.continent and each.continent != "null":
                    print("Circuit Case3 Yo!")
                    circuitousness = 1

        return circuitousness

    def analyzeCase3(self):
        # Case 3: Src and Dst are in the same continent, intermediate hop is outside continent
        print("**** Analyze Case 3: ****")
        # get source and destination continent
        print("Source continent:", self.srcGeo.continent)
        print("Destination continent:", self.dstGeo.continent)

        # verify that source and dst continent are different

        # loop through each hop
            # look at continent of intermediate hop
            # if hop is not srcContinent or dstContinent, output the hop - (IP, AS, Country, Continent)
        itemInd = 0
        for item in self.hopListGeo:
            print('Hop #', itemInd, ':', self.hopList[itemInd].hopAddr, "-", self.hopListGeo[itemInd].country, ",", self.hopListGeo[itemInd].continent)
            if item.continent!="null" and (item.continent != self.srcGeo.continent) and (item.continent != self.dstGeo.continent):
                print('Hop #', itemInd, '---- case 3 hop ----')
                # check RTT difference between this hop and the one before it
                if self.hopList[itemInd].isError == 0 and self.hopList[itemInd-1].isError == 0:
                    if hasattr(self.hopList[itemInd], 'hopMean') and hasattr(self.hopList[itemInd-1], 'hopMean'):
                        hopDiff = self.hopList[itemInd].hopMean - self.hopList[itemInd-1].hopMean
                        print('Hop mean RTT:', self.hopList[itemInd].hopMean)
                        print('Delta RTT =', hopDiff)
                        hopThreshold = 80
                        if hopDiff >= 80:
                            print('Delta RTT is above threshold')
                        else:
                            print('DeltaRTT is below threshold, likely a false positive result')

                    else:
                        print('Could not calculate delta RTT')

                else:
                    print('Could not calculate delta RTT')

                print('This hop is outside the src and dst continent:', item.continent)
                print('Hop IP:', self.hopListAS[itemInd].ipAddr)

                if self.hopListAS[itemInd].ipToASLookupSucceed == 1:
                    print('Hop AS#:', self.hopListAS[itemInd].asNumber)
                    print('Hop Country (from AS lookup):', self.hopListAS[itemInd].country)
                else:
                    print('Hop AS info - country and AS# unsuccessful for this hop!')

                print('Hop Country (from GeoIP lookup):', item.country)
            itemInd = itemInd+1

    def csvWrite(self, row, path):
        writer = csv.writer(path)
        writer.writerow(row)
        return

    def __init__(self, csvRow, case1filePath, case2filePath, case3filePath):
        self.isError = 0

        self.csvRow = csvRow    # store the raw row / not really necessary
        # print("csvline = ",self.csvRow)

        # destination and source IP addrs are the 1st and 2nd value in the csv
        self.dstIP = self.csvRow[0]
        self.srcIP = self.csvRow[1]

        # the rest of the values are intermediate hops
        # each hop should have 3 attempts (and 3 corresponding RTTs)
        self.hopList = []
        # print("length of csvRow=",len(self.csvRow))

        # loop through the rest of the values after dstIP and srcIP
        # this loop logic assumes 3 attempts per hop!
        for i in range(2, len(self.csvRow)-2, 3):
            hop = hopInfo(self.csvRow[i], self.csvRow[i+1], self.csvRow[i+2])
            self.hopList.append(hop)

        if self.isError == 0:

            # get GEO ip on src, dst, and hops
            self.dstGeo = geoIP(self.dstIP)
            self.srcGeo = geoIP(self.srcIP)

            self.hopListGeo = []
            for hop in self.hopList:
                self.hopListGeo.append(geoIP(hop.hopAddr))

            self.hopListAS = []
            for hop in self.hopList:
                # time.sleep(0.1) # throttle asLookup default=0.25s
                asResult = asLookup(hop.hopAddr, 2)
                self.hopListAS.append(asLookup(hop.hopAddr, 2))

                # print('AS Number =', self.hopListAS[-1].asNumber)


            # print(self.hopListAS[:])

            # print("------INFO------")
            # print("Source:", self.srcGeo.country, self.srcGeo.continent)
            # print("Destination:", self.dstGeo.country, self.dstGeo.continent)

            # Check our three cases of circuitousness:
            case1status = self.checkCase1()
            if case1status == 1:
                self.case = 1
                self.analyzeCase1()
                self.csvWrite(csvRow, case1filePath)
                # csvwrite csvRow here

            case2status = self.checkCase2()
            if case2status == 1:
                self.case = 2
                self.analyzeCase2()
                self.csvWrite(csvRow, case2filePath)

            case3status = self.checkCase3()
            if case3status == 1:
                self.case = 3
                self.analyzeCase3()
                self.csvWrite(csvRow, case3filePath)

            # print("------END-----")


# TRACEROUTE FILE TO BE ANALYZED:
csvFilePath = open(home+'/cse534/data/regional_combined/combined_filtered_80.csv')
csvFile = csv.reader(csvFilePath, delimiter=';')

# PATH OF OUTPUT LOG FILES:
# output instances of case1/2/3 to csv:-
case1filePath = open(home+'/cse534/output/case1/case1.csv', 'r+')
case2filePath = open(home+'/cse534/output/case2/case2.csv', 'r+')
case3filePath = open(home+'/cse534/output/case3/case3.csv', 'r+')

# LOOP THROUGH EACH ROW IN THE TRACEROUTE FILE - EACH ROW IS A TRACEROUTE
rowNum = 0
for row in csvFile:
    print("--------------------------------------------------------------Row #", rowNum)
    result = traceRt(row, case1filePath, case2filePath, case3filePath)
    rowNum = rowNum + 1

print('Done!')
case1filePath.close()
case2filePath.close()
case3filePath.close()