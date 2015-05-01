from asLookup import asLookup

ip = "8.8.8.8"
AS = asLookup(ip, 2)

print(AS.asName)
