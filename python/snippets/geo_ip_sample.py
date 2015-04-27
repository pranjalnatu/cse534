import geoip2.database


# Using geoip2 package: https://pypi.python.org/pypi/geoip2
# GeoIP database provided by MaxMind (GeoLite2): http://dev.maxmind.com/geoip/geoip2/geolite2/

# GEO IP SAMPLE TEST:
reader = geoip2.database.Reader('/Users/justinchan/PycharmProjects/africa/geo_db/GeoLite2-City.mmdb')

response = reader.city('129.49.122.166')

print(response.city.name)
print(response.country.name)
print(response.location.latitude)
print(response.location.longitude)
print(response.continent.names['en'])
print(response.continent.code)