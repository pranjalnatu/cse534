__author__ = 'justinchan'


file="192.168.1.1"


my_string = "blah, lots  ,  of ,  spaces, here "
a = [x.strip() for x in my_string.split(',')]
print(a)


ip="192.168.1.101"
b= [x.strip() for x in ip.split('.')]
print(b[3])