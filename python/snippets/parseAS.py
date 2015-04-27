__author__ = 'justinchan'
import re


asFile = open('/Users/justinchan/PycharmProjects/cse534/data/raw/regional_ASpaths_snippet.txt')


line = asFile.readline()
print("whole line:",line)

# string = '"Foo Bar" "Another Value"'

sampleString = '[1668, 50448, 3267, 197467]	1668'
string = line
print(re.findall(r'\[(.*?)\]', string))
asString = re.findall(r'\[(.*?)\]', string)
asList = [x.strip() for x in asString[0].split(',')]
print(asList)

for asItem in asList:
    print(asItem)
