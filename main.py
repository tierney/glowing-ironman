from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import bz2
import os
import sys
import json

from credentials import *

class StdOutListener(StreamListener):
  """ A listener handles tweets are the received from the stream.
  This is a basic listener that just prints received tweets to stdout.

  """
  def __init__(self, fout):
    self.fout = fout

  def on_data(self, data):
    self.fout.write(json.dumps(json.loads(data)) + '\n')
    return True

  def on_error(self, status):
    print 'Error', status

if __name__ == '__main__':
  fnout = sys.argv[1]

  if os.path.exists(fnout):
    print 'Path already exists: ', fnout
    sys.exit(1)

  with bz2.BZ2File(fnout,'wb') as fh:
    l = StdOutListener(fh)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.sample()

