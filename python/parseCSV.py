import csv
import geoip2.database

geoDB = geoip2.database.Reader('/Users/justinchan/PycharmProjects/africa/geo_db/GeoLite2-City.mmdb')

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

        '''
        print("hopAddr:",self.hopAddr)
        print("hopRTT1:",self.hopRTT1)
        print("hopRTT2:",self.hopRTT2)
        print("hopRTT3:",self.hopRTT3)
        '''

class traceRt:

    def __init__(self, csvRow):
        self.csvRow = csvRow
        print("csvline = ",self.csvRow)
        self.dstIP = self.csvRow[0]
        self.srcIP = self.csvRow[1]

        self.hopList = []

        print("length of csvRow=",len(self.csvRow))
        for i in range(2, len(self.csvRow)-2, 3):
            hop = hopInfo(self.csvRow[i], self.csvRow[i+1], self.csvRow[i+2])
            self.hopList.append(hop)

        '''
        print(self.hopList[0].hopAddr)
        print(self.hopList[1].hopAddr)
        print(self.hopList[2].hopAddr)
        '''

        # get GEO ip on src, dst, and hops
        self.dstGeo = geoIP(self.dstIP)
        self.srcGeo = geoIP(self.srcIP)

        self.hopListGeo = []
        for hop in self.hopList:
            self.hopListGeo.append(geoIP(hop.hopAddr))


        print("------INFO------")
        print("Source:", self.srcGeo.country, self.srcGeo.continent)
        print("Destination:", self.dstGeo.country, self.dstGeo.continent)

        for each in self.hopListGeo:
            print("Hop:", each.country, each.continent)
        print("------END-----")


csvFilePath = open('/Users/justinchan/PycharmProjects/cse534/data/csv/1765618.csv')
csvFile = csv.reader(csvFilePath, delimiter=';')

for row in csvFile:
    traceRt(row)