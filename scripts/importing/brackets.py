#!/usr/bin/python
import re # Regular Expressions
import collections # Data Types
import sys # File operations
import codecs # UniCode support
import nltk

# Open the flat text file
f = codecs.open("brackets.txt", 'r', encoding='utf-8')

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
        pos = u'UNSP' # Default tag

        
        if len(a) == 3: # If tag present
            pos = a[2] # Set to tag provided

        # Unpack slashes
        if '/' in literal:
            m = re.search(r'der\/die\/das([\w]+)', literal)
            stem = m.group(1)
            literal = 'der'+stem+',die'+stem+',das'+stem

        # Unpack brackets
        if '(' in literal:
            m = re.search(r'(.+)\((.+)\)', literal)
            stem = m.group(1).encode('utf-8')
            endings = m.group(2).encode('utf-8').split(',')
            variants = []
            variants.append(stem) # Stem itself also a word, e.g. ein, eine
            for ending in endings:
                variants.append(stem + ending)
            literal = ','.join(variants)

        # Resolve multiple headwords
        literal_array = literal.split(',')
        if len(literal_array) > 1:
            print repr(literal_array)

        count += 1

    except IndexError:
        sys.stderr.write( "Something wrong this this line: " + line + '\n')
        continue

f.close() # Close flat file

print "Hooray!", count
