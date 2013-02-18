import sys
import re
import os
import collections
import codecs # UniCode support
from pymongo import Connection # For DB Connection
from pymongo.errors import ConnectionFailure # For catching exeptions
import nltk

DIR = os.path.abspath(os.path.dirname(__file__))

def copy_morphy():
  
  # MongoDB connection
  try:
    db_conn = Connection(host="localhost", port=27017) # Here we specified the default parameters explicitly
    print "Connected to MongoDB successfully!"
  except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)

  # Grab a database
  db = db_conn["lab"]

  # Open file
  f = codecs.open(os.path.join(DIR, "morphy.txt"), 'r', encoding='utf-8') # Codecs instead regular 'open' to handle UTF-8

  # Read each line
  for line in f:
    
    try: # For exception catching
      a = line.rstrip().split('\t') # In this case, it's space-separated!

      # If a column is missing...
      if len(a) is not 2:
        raise IndexError
      
      raw_form = a[0]
      immediate = a[1]

      if not immediate.isalpha() and '-' not in immediate:
        immediate = raw_form


      # Create dictionary object
      record = {
        "vollform": raw_form,
        "immediate": immediate
      }
      
      # Insert document into DB
      db.morphy.insert(record, safe=True) # Collections ('morphy' here) are lazily created
      
    # Exception handler
    except IndexError:
      sys.stderr.write( "Something wrong with this line: " + line + '\n')
      continue
    
  # Close file
  f.close()

  print 'Hooray!'
  
if __name__ == "__main__":
  copy_morphy()