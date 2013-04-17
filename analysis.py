#/usr/bin/env python

import sys
import json
import bz2
import datetime
#Untested code
#start using this soon rather than just tracking plain old tweet IDs
class Node:
  text
  dateANDtime

  def stringMonth2int(s):
    if s == "Jan": return 1
    if s == "Feb": return 2
    if s == "Mar": return 3
    if s == "Apr": return 4
    if s == "May": return 5
    if s == "Jun": return 6
    if s == "Jul": return 7
    if s == "Aug": return 8
    if s == "Sep": return 9
    if s == "Oct": return 10
    if s == "Nov": return 11
    if s == "Dec": return 12
    return 13 #this will cause a failure

  def setTime(s):
    #Mon Mar 11 15:30:27 +0000 2013 -> datetime object
    slist = s.split(" ")
    #year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]
    timelist = slist[3].split(":")
    dateANDtime = datetime.datetime.datetime(int(slist[5]), stringMonth2int(slist[1]), int(slist[2]), int(timelist[0]), int(timelist[1]), int(timelist[2]))
    
    def setText(s): 
      text = s

class Driver:

  #id -> set of id  map, like a set of production rules
  #id -> [id,id...]
  #id -> [id]
  #...
  id2sets = dict()
  #set of all entries;determining if an id is a root or not requires we either 
  #search all mappings to determine if we've ever seen it, or maintain some 
  #way of answering that question
  universe = set()
  #set of roots
  rootset = set()

  def update_mappings(id,rid):
    if rid in id2sets:
      #add to set (branch in flow), & add it to set of all know id's (so we know
      #it is not a root in future)
      id2sets[rid] = id2sets[rid].add(id)
      universe.add(id)
    else:
      #add to keys and start new mapping (continuation of a flow), and make note
      #of it being a new root & add it to set of all known id's (next 3 lines
      #fail if attempted as 1 line)
      temps = id2sets[rid]
      temps.add(id)
      id2sets[rid] = temps
      #check for pre-existence in any set and add to set of roots if it is new
      if rid not in universe:
        rootset.add(rid)
        universe.add(rid)
      universe.add(id)

  def ProcessTweet(tweet, diction):
    if 'retweeted_status' in tweet.keys():
      #id is is unique id of this tweet, a retweet of a prior tweet
      id = tweet['id']
      #rid is the unique id of the tweet that is being retweeted
      rid = tweet['retweeted_status']['id']
      update_mappings(id, rid, diction)


  #somewhat pretty print the dictionary--fixed bug from prior file
  def printDictionary(f, d):
  outfile = open(f,'w')
  keys = d.keys()
  for k in keys:
    mapping = d[k]
    outfile.write("\n")
    outfile.write(str(k))
    outfile.write(" ->\t")
    max = len(mapping)
    for x in range(max):
      if x > 0: print "\n\t\t | "
      listchain = mapping[x]
      for elem in listchain:
        outfile.write(str(elem))
        outfile.write(", ")
  outfile.flush()
  outfile.close()

  def printDictionary_toScreen(d):
    keys = d.keys()
    for k in keys:
      mapping = d[k]
      print("\n")
      print(str(k))
      print(" ->\t")
      max = len(mapping)
      for x in range(max):
        if x > 0: print " | "
        listchain = mapping[x]
        for elem in listchain:
          print(str(elem))
          print(", ")

  def process_TweetsFromFile(fnout, outfile):
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
      #print the dictionary to out file even if we interrupt further progress
      except KeyboardInterrupt:
        printDictionary(outfile,d)
        raise KeyboardInterrupt
    printDictionary(outfile,d)

  #incase have to 2 go to file to get it, but this would be slow
  def getTweetText(id, f):
    for line in f:
      if 'id' in tweet.keys():
        tid = tweet['id']
        if id == tid:
          if 'text' in tweet.keys():
            return tweet['text']


  
def main(argv):
  driver = Driver()
  #First argument is the data file to read.
  #Second argument is the data file to which to write upon completion or 
  #interruption
  process_TweetsFromFile(argv[1],argv[2])


if __name__=='__main__':
  main(sys.argv)
