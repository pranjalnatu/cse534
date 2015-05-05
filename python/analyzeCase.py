import csv
import csv
import geoip2.database
import numpy as np

from IPy import IP
from asLookup import asLookup
from os.path import expanduser
home = expanduser("~")

geoDB = geoip2.database.Reader(home+'/cse534/GeoLite2-City.mmdb')




class analyzeCase():
    def analyzecase1(self, csvline):
        #############################
        #       CASE No. 1
        # Check if src & dst are in same country and one of the hops is in a different country
        ############################

        # get source and destination country

        # verify that source and dst ctry are the same

        # loop through each hop
            # look at country of each intermediate hop
            # if hop is out of country, output the hop - (IP, AS, Country)


        return

    def analyzecase2(self, csvline):
        ##########################
        #       CASE No. 2
        # Check if src & dst are in the same continent and one of the hops is in a different continent
        ##########################

        # get source and destination continent

        # verify that source and dst ctry are the same

        # loop through each hop
            # look at continent of intermediate hop
            # if hop is outside of the continent, output the hop - (IP, AS, Country, Continent)

        return

    def analyzecase3(self, csvline):
        #############################
        #       CASE No. 3
        # Check if src & dst are in continents A & B and one of the hops is in a continent C such that C != A && C != B
        ############################

        # get source and destination continent

        # verify that source and dst continent are different

        # loop through each hop
            # look at continent of intermediate hop
            # if hop is not srcContinent or dstContinent, output the hop - (IP, AS, Country, Continent) 

        return

    def __init__(self):


        print("init done")


casefilepath = open(home+'/csv534/output/case1/case1.csv')
casefile = csv.reader(casefilepath, delimiter=',')




