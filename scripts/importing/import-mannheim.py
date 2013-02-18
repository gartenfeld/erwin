#!/usr/bin/python
import re # Regular Expressions
import collections # Data Types
import sys # File operations
import codecs # UniCode support
import os
import nltk
from pymongo import Connection # For DB Connection
from pymongo.errors import ConnectionFailure # For catching exeptions

DIR = os.path.abspath(os.path.dirname(__file__))

def process_mannheim():

  # MongoDB connection
  try:
    db_conn = Connection(host="localhost", port=27017) # Here we specified the default parameters explicitly
    print "Connected to MongoDB successfully!"
  except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)

  # Grab a database
  db = db_conn["lab"]

  # Open the flat text file
  f = codecs.open(os.path.join(DIR, "mannheim.txt"), 'r', encoding='utf-8')

  count = 0

  # For each line of the file
  for line in f:
    try:
      # Strip trailing spaces, then split by space
      a = line.rstrip().split(' ') # The result 'a' is a list

      literal = a[0]
      freq_band = a[1]
      pos = u'UNSP' # Default tag


      if len(a) == 3: # If tag present
        pos = a[2] # Set to tag provided

      # Unpack slashes
      if '/' in literal:
        m = re.search(r'der\/die\/das([\w]+)', literal)
        stem = m.group(1)
        literal = unicode('der'+stem+',die'+stem+',das'+stem)

      # Unpack brackets
      if '(' in literal:
        literal = unpack_brackets(literal)
        literal = unicode(literal)

      if isinstance(literal, str):
        literal = literal.decode('utf-8')


      # Set up the dictionary
      rank = count + 1
      band = freq_band
      wortart = pos
      grundform = literal
      vollformen = []

      # Resolve multiple headwords
      literal_array = literal.split(',')

      if len(literal_array) > 1:
        shortest = 100
        grundform = u"NOTFOUND"

        for variant in literal_array:

          # if vollform can be found
          if db.morphy.find({"vollform":variant}).limit(1).count()>0:
            l = db.morphy.find({"vollform":variant}).limit(1)
            new_lookup = l[0].get("immediate")

            if len(new_lookup)< shortest:
              grundform = new_lookup
              shortest = len(new_lookup)
          # if vollform cannot be found, try find grundform
          elif db.morphy.find({"immediate":variant}).limit(1).count()>0:
            if len(variant)< shortest:
              grundform = variant
              shortest = len(variant)
          else:
            grundform = variant
            vollformen += literal_array
        # end of for loop checking conflicting headwords

      vollformen.append(grundform)

      #Search for and add fullforms
      fullforms = db.morphy.find({"immediate":grundform},{"vollform":1})
      for doc in fullforms:
        form = doc.get("vollform")
        vollformen.append(form)

      # Construct dictionary
      entry = { "rank" : rank, 
                "band" : band,
             "wortart" : wortart,
           "grundform" : grundform,
          "vollformen" : vollformen }

      # Insert document into DB
      db.mannheim.insert(entry)
      
      if count % 1000 == 0:
        print count

    # end of try
    except IndexError:
      sys.stderr.write( "Something wrong this this line: " + line)
      continue
    count += 1
  # end of for loop
  f.close() # Close flat file

  print "Hooray!", count

def unpack_brackets(literal):
  m = re.search(r'(.+)\((.+)\)', literal)
  stem = m.group(1).encode('utf-8')
  endings = m.group(2).encode('utf-8').split(',')
  variants = []
  #variants.append(stem) # Stem itself also a word, e.g. ein, eine
  for ending in endings:
    variants.append(stem + ending)
    literal = ','.join(variants)
  literal = literal.decode('utf-8')
  return literal

if __name__ == "__main__":
  process_mannheim()