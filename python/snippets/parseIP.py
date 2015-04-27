__author__ = 'justinchan'


file="192.168.1.1"


my_string = "blah, lots  ,  of ,  spaces, here "
a = [x.strip() for x in my_string.split(',')]
print(a)


ip="192.168.1.101"
b= [x.strip() for x in ip.split('.')]
print(b[3])


testString="23.45.145.228,rtt=119.756 23.45.145.228,rtt=119.783 23.45.145.228,rtt=119.672"
c = [x.strip() for x in testString.split(' ')]
print(c)

for item in c:
    d = [x.strip() for x in item.split(',')]
    d[1] = d[1][4:]
    print(d)
