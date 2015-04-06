from pandas import DataFrame, read_csv
import geoip2.database
import pandas as pd
import csv

# Using geoip2 package: https://pypi.python.org/pypi/geoip2
# GeoIP database provided by MaxMind (GeoLite2): http://dev.maxmind.com/geoip/geoip2/geolite2/

reader= geoip2.database.Reader('/Users/justinchan/PycharmProjects/africa/geo_db/GeoLite2-City.mmdb')

response = reader.city('129.49.122.166')

print(response.city.name)
print(response.country.name)
print(response.location.latitude)
print(response.location.longitude)

#hops = pd.read_csv('/Users/justinchan/PycharmProjects/africa/traceroute_csv/test.csv')
#hops = pd.DataFrame.from_csv('/Users/justinchan/PycharmProjects/africa/traceroute_csv/extraced_IP.csv', sep=',')
#hops = pd.DataFrame.from_csv('/Users/justinchan/PycharmProjects/africa/traceroute_csv/extraced_IP_test.csv', sep=',', tupleize_cols=True)


f = open('/Users/justinchan/PycharmProjects/africa/traceroute_csv/extraced_IP.csv')
csv_f = csv.reader(f)

for row in csv_f:
    print(row)
    print("Number of hops: len(row))
    for col in row:
        if col !="":
            try:
                response = reader.city(col)
                print(response.country.name)
            except geoip2.errors.AddressNotFoundError:
                print("*Local IP*")
            except ValueError:
                print("VALUE ERROR")




