#/usr/bin/env python

import sys
import json
import bz2

def main(argv):
  fnout = argv[1]
  fopen = open
  if fnout.endswith('.bz2'):
    fopen = bz2.BZ2File

  with fopen(fnout, 'rb') as fh:
    for line in fh:
      loaded = json.loads(line)
      to_print = []
      if 'retweeted_status' in loaded.keys():
        # print json.dumps(loaded['retweeted_status']['user'], indent = 2)
        # to_print.append(loaded['retweeted_status']['id'])
        print loaded['retweeted_status']['user']['screen_name'],
        print ',',
        print loaded['retweeted_status']['user']['followers_count'],
        print ',',
        print loaded['retweeted_status']['text'].encode('utf-8').replace('\n',' '),
        print

      #print loaded.keys()
      #print loaded['retweeted']
      #print loaded['retweet_count']
      # print json.dumps(loaded, indent = 2)
      # print loaded['entities']

if __name__=='__main__':
  main(sys.argv)
