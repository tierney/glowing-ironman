#/usr/bin/env python

import sys
import json
import bz2

#in retrospect, this task is like (not binary but b-)tree reconstruction given 
#many nodes with pointers to children (retweet ids and ids). We could end up 
#with many trees, of various degrees of bushiness and depth, and we have no idea 
#which elements are the roots of each tree. But perhaps that approach would be 
#better than lists of lists, as below, which represent paths to leaves from 
#higher nodes that may or may not be roots. 

#possibly super slow dumb way of doing this...
def exists_anywhere(rid,d):
  #double iterate over id list list for every key to find the id
  #anywhere it might exist (we already know it is not a key)...super slow operation
  for ids in d:
    listlist = d[ids]
    max = len(listlist)
    for x in range(max):
      l = listlist[x]
      max2 = len(l)
      for y in range(max2):
        item = l[y]
        if item == rid:
          print "===Found a continuation in a retweet chain from id: " + str(rid) + "==="
          #since we need to return to this location again to update it, 
          #return a tuple to save time and spare us a second search
          #tell us key under which id exists, which list, which element of that list
          return (True, ids, x, y)
  #print "Didn't find any continuation for id:" + str(rid)
  return (False, -1,-1,-1)

#check what is the mapping of id and update accordingly
def update_key_mapping(id,rid,d):
  #already know rid is a key in d
  listoflists = d[rid]
  #id must be appended to mapping of rid as single element in its own list
  listoflists.append([[id]])
        
#given a location, go to that location and insert the retweet id either at end of an existing list
#if possible, else as the terminal of a new list, reflecting a fork (branch) in a retweet flow
def update_list_mapping(id,rid,d, locationTuple):
  print "\tupdate_list_mapping..."
  key = locationTuple[1]
  nthlist = locationTuple[2]
  nthelement = locationTuple[3]
  #go to the location
  listlist = d[key]
  thelist = listlist[nthlist]
  #if nthelement is also last, just append to end of list
  if locationTuple[3] == len(thelist):
    thelist.append(id)
  else:
  #else have a fork; have to duplicate all elements up to this element, then append, then append again
    newflow = thelist[0:(locationTuple[3])]
    newflow.append(id)
    listlist.append(newflow)

#if a key in the dictionary turns out to be itself a retweet and we now have the prior tweet
#this might actully be unneccessary but not seen enough twitter data to convince myself--nor found
#any source to tell me--that this isn't possible, ie. that retweets are always nested but only 1 level
#at maximum
def update_pushkey_mapping(id,rid,d):
  print "\tupdate_pushkey_mapping..."
  #in this case a retweet rid is being retweeted in a more recent tweet with id, but our dictionary
  #has id as a key (a starting point). So the key must be replaced by rid and id prepended to 
  #all the entries in the list of id lists, like so:
  lists = d[id]
  fixedlists = []
  for l in lists:
    fixedlists.append([id] + l)
  del d[id]
  d[rid] = fixedlists

def update_dictionary(id, rid, d):
  #print "Updating the dictionary..."
  #case I: if d has id -> id list list mapping, update the mapping
  if rid in d:
    update_key_mapping(id,rid,d)
    return
  if id in d:
    update_pushkey_mapping(id,rid,d)
    return
  #else
  #case II & III: if d has no id -> id list list mapping, check for existence of id anywhere else
  locationTuple = exists_anywhere(id,d)
  if locationTuple[0]:
    #case II: if id exists anywhere, update the mapping, forking if need be
    update_list_mapping(id,rid,d, locationTuple)
  else:
    #case III: if d has no id -> id list list mapping and it doesn't appear anywhere else
    #then add it as a new key -> id list list mapping with rid as the only element in the only list
    #to which the key maps
    d[rid]=([[id]])



def ProcessTweet(tweet, diction):
  # Searches for retweeted status in tweet dict's keys.
  if 'retweeted_status' in tweet.keys():
    #id is is unique id of this tweet, a retweet of a prior tweet
    id = tweet['id']
    #rid is the unique id of the tweet that is being retweeted
    rid = tweet['retweeted_status']['id']
#    print "\n---PROCESSING A RETWEET ---"
#    print " ID: "
#    print id
#    print " TIME: "
#    print tweet['retweeted_status']['created_at']
#    print ', RETWEET ID:',
#    print rid
    update_dictionary(id, rid, diction)

def printDictionary(f, d):
  outfile = open(f,'w')
  keys = d.keys()
  for k in keys:
    mapping = d[k]
    outfile.write("\n")
    outfile.write(str(k))
    outfile.write(" ->\t")
    for listchain in mapping:
      for elem in listchain:
        outfile.write(str(elem))
        outfile.write(", ")
    outfile.write("\n\t\t | ")
  outfile.flush()
  outfile.close()


def main(argv):
  #use a dictionary to map from IDs to lists of lists of retweet IDs
  d = dict()
  # First argument is the data file to read.
  fnout = argv[1]
  # Second argument is the data file to which to write upon completion or interruption
  outfile = argv[2]
  # Figure out which function should open the file.
  fopen = open
  if fnout.endswith('.bz2'):
    fopen = bz2.BZ2File


  with fopen(fnout, 'rb') as fh:
    # Process every line as its own JSON tweet.
    for line in fh:
      try:
        loaded = json.loads(line)
        ProcessTweet(loaded, d)
      except KeyboardInterrupt:
        printDictionary(outfile,d)
        raise KeyboardInterrupt
    printDictionary(outfile,d)
if __name__=='__main__':
  main(sys.argv)
