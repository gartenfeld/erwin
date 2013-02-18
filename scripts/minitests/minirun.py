#!/usr/bin/python
import re # Regular Expressions
import collections # Data Types
import sys # File operations
import codecs # UniCode support
import nltk

# Open the flat text file
f = codecs.open("miniband.txt", 'r', encoding='utf-8')

count = 0

# For each line of the file
for line in f:

    try:
        # Strip trailing spaces, then split by space
        a = line.rstrip().split(' ') # The result 'a' is a list

        # If a column is missing...
        #if len(a) is not 2:
            #raise IndexError
      
        literal = a[0]
        band = a[1]
        pos = 'UNSP'

        if len(a) == 3:
            pos = a[2]
            # print literal, band, pos

        if not literal.isalpha():
            print literal, band, pos

        count += 1

    except IndexError:
        sys.stderr.write( "Something wrong this this line: " + line + '\n')
        continue

f.close() # Close flat file

print "Hooray!", count
