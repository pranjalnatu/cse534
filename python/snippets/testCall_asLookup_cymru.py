from asLookup import asLookup

ip = "216.58.219.206"
ASnumber = "AS12"
AS = asLookup(ip, 2)

print(AS.asName)
