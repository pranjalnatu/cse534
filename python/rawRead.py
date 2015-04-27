from pprint import pprint
# import json
import simplejson
import geoip2.database


# Using geoip2 package: https://pypi.python.org/pypi/geoip2
# GeoIP database provided by MaxMind (GeoLite2): http://dev.maxmind.com/geoip/geoip2/geolite2/
__author__ = 'justinchan'

reader = geoip2.database.Reader('/Users/justinchan/PycharmProjects/africa/geo_db/GeoLite2-City.mmdb')

dataFile = open('/Users/justinchan/PycharmProjects/africa/raw_traceroute/1765622.json')
# dataFile = open('/Users/justinchan/PycharmProjects/cse523/testdata/1963271.log')

data = simplejson.load(dataFile)
pprint(data)

srcNotFound = 0
dstNotFound = 0
numItems = 0
for item in data:
    numItems += 1
    src = item.get('src_addr')
    dst = item.get('dst_addr')
    try:
        srcCountry = reader.city(src).country.name
    except geoip2.errors.AddressNotFoundError:
        srcCountry = "Not Found"
        srcNotFound += 1
    except ValueError:
        srcCountry = "Value Error"
    except:
        continue

    try:
        dstCountry = reader.city(dst).country.name
    except geoip2.errors.AddressNotFoundError:
        dstCountry = "Not Found"
        dstNotFound += 1
    except ValueError:
        dstCountry = "Value Error"
    except:
        dstCountry = "Other Error"
        print("=====dest =",dst)

    print(srcCountry,"--",dstCountry)

    for item in item.get('result'):
        # print(item)
        item["result"][]



print("srcNotFound=",srcNotFound,"dstNotFound=",dstNotFound)
print("numItems=",numItems)