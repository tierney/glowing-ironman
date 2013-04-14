#/usr/bin/env python

import sys
import json
import bz2

#possibly super slow dumb way of doing this...
def exists_anywhere(id,d):
  #double iterate over id list list for every id key to find the id
  #anywhere it might exist (we already know it is not a key)...super slow operation
  for ids in d:
    listlist = d[ids]
    max = len(listlist)
    for x in range(max):
      l = listlist[x]
      max2 = len(l)
      for y in range(max2):
        item = l[y]
        if item = id:
          print "\nFound a continuation in a retweet chain from id: " id
          #since we need to return to this location again to update it, 
          #return a tuple to save time and spare us a second search
          return (True, ids, x, y)
  print "\nDidn't find any continuation for id:" id
  return (False, -1,-1,-1)

#check what is the mapping of id and update accordingly
def update_key_mapping(id,rid,d):
  #already know id is a key in d
  listoflists = d[id]
  #find where it might fit into mapping, forking an existing list of ids if needed
  for l in listlist:
    for item in l:
      if item = id:

def update_dictionary(id, rid, d):
  #case I: if d has id -> id list list mapping, update the mapping
  if id in d:
    update_key_mapping(id,rid,d)
  else:
  #case II & III: if d has no id -> id list list mapping, check for existence of id anywhere else
    locationTuple = exists_anywhere(id,d)
    if locationTuple[0]:
      #case II: if id exists anywhere, update the mapping, forking if need be
      update_list_mapping(id,rid,d, locationTuple)
    else:
      #case III: if d has no id -> id list list mapping and it doesn't appear anywhere else
      #then add it as a new key -> id list list mapping with rid as the only element in the only list
      #to which the key maps
      d[id]=([[rid]])



def ProcessTweet(tweet, diction):
  # Searches for retweeted status in tweet dict's keys.
  if 'retweeted_status' in tweet.keys():
    id = tweet['id']
    rid = tweet['retweeted_status']['id']
    print "\n---PROCESSING A RETWEET ---\n"
    print " ID: "
    print id
    print " TIME: "
    print tweet['retweeted_status']['created_at']
    print ', RETWEET ID:',
    print rid
    update_dictionary(id, rid, diction)

      


def main(argv):
  #use a dictionary to map from IDs to lists of lists of retweet IDs
  d = dict()
  # First argument is the data file to read.
  fnout = argv[1]

  # Figure out which function should open the file.
  fopen = open
  if fnout.endswith('.bz2'):
    fopen = bz2.BZ2File


  with fopen(fnout, 'rb') as fh:
    # Process every line as its own JSON tweet.
    for line in fh:
      loaded = json.loads(line)
      ProcessTweet(loaded)


if __name__=='__main__':
  main(sys.argv)
