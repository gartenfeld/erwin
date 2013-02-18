#!/usr/bin/python
import re # Regular Expressions
import collections # Data Types
import sys # File operations
import os
import codecs # UniCode support
import nltk
from collections import defaultdict

DIR = os.path.abspath(os.path.dirname(__file__))

def make_dict():

    # Open the flat text file
    f = codecs.open(os.path.join(DIR, "morphy.txt"), 'r', encoding='utf-8')

    count = 0
    q_mark = 0
    lemmas = []

    # For each line of the file
    for line in f:

        try:
            # Strip trailing spaces, then split by space
            a = line.rstrip().split('\t') # The result 'a' is a list

            # If a column is missing...
            if len(a) is not 2:
                raise IndexError
          
            raw_form = a[0]
            immediate = a[1]
            lemmas.append(immediate)

            if not raw_form.isalpha() and '-' not in raw_form:
                print raw_form

            if not immediate.isalpha() and '-' not in immediate:
                print raw_form, immediate
                q_mark += 1

            count += 1

        except IndexError:
            sys.stderr.write( "Something wrong this this line: " + line + '\n')
            continue

    f.close() # Close flat file

    print "Hooray!", count, q_mark, len(set(lemmas))

if __name__ == '__main__':
    make_dict()
