#/usr/bin/env python

import sys
import json
import bz2


def ProcessTweet(tweet):
  # Searches for retweeted status in tweet dict's keys.
  if 'retweeted_status' in tweet.keys():
    print tweet['retweeted_status']['user']['screen_name'],
    print ',',
    print tweet['retweeted_status']['user']['followers_count'],
    print ',',
    print tweet['retweeted_status']['text'].encode('utf-8').replace('\n',' '),
    print


def main(argv):
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
