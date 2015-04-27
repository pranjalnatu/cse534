__author__ = 'justinchan'

import geoip2.database
import simplejson
from pprint import pprint

# RIPE Atlas raw data structure documentation
# https://atlas.ripe.net/docs/data_struct/#v4570_traceroute


class traceRt:

    def geoIP(self, ipAddr, type):
        try:
            response = self.geoDB.city(ipAddr)
            if type == 1: # Return country name
                name = response.country.name
            elif type == 2: # Return continent name
                name = response.continent.names['en']
            else:
                print("geoIP: Specify country or continent!")
        except geoip2.errors.AddressNotFoundError:
                name = "Not Found"

        return name

    def hopParse(self, hopResult):
        # Parse through result list.
        # Each item in list contains results dict for each hop
        print("Entering hopParse:")

        for hop in hopResult:
            print("Hop #", hop['hop'])
            for hopTry in hop['result']:


                if 'rtt' in hopTry.keys():
                    # reply case
                    print(hopTry['rtt'])
                else:
                    # timeout case
                    # pprint(hopTry)

    def __init__(self, rawTrace):
        self.geoDB = geoip2.database.Reader('/Users/justinchan/PycharmProjects/africa/geo_db/GeoLite2-City.mmdb')
        self.rawTrace = rawTrace
        self.isValid = True

        # Get source and destination IPs
        self.src_addr = rawTrace.get('src_addr')
        self.dst_addr = rawTrace.get('dst_addr')


        if (self.src_addr==None) |(self.dst_addr==None):
            print("src_addr or dst_addr is empty. Skipping hop parsing")
            pprint(self.rawTrace)
            self.isValid = False

        if self.isValid:
            # Geolocate source and destination countries/continents
            self.srcCountry = self.geoIP(self.src_addr, 1)
            self.srcContinent = self.geoIP(self.src_addr, 2)
            self.dstCountry = self.geoIP(self.dst_addr, 1)
            self.dstContinent = self.geoIP(self.dst_addr, 2)

            pprint(rawTrace.get('result'))
            self.hopParse(rawTrace.get('result'))

            # Parse through each hop dict in result list
            # for item in rawTrace.get('result'):





dataFile = open('/Users/justinchan/PycharmProjects/africa/raw_traceroute/1765622.json')
data = simplejson.load(dataFile)

for item in data:
    traceRt(item)