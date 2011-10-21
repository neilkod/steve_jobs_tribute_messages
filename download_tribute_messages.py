#!/usr/bin/python
import urllib2
import simplejson as json
import time
import codecs

# a page on apple's site shows the # of messages available
# start with 0 and retrieve up to message_range messages
metadata = json.loads(urllib2.urlopen('http://www.apple.com/stevejobs/messages/main.json').read())
message_range = int(metadata['totalMessages'])
print '%s total messages to download:' % message_range


# the url for each message. i learned of this url by inspecting
# the network calls to http://www.apple.com/stevejobs
# using chrome's developer tools
url="http://www.apple.com/stevejobs/messages/%d.json" 

# create our destination file
# i'm using codecs because it does a better job at handling international characters
output_file = 'stevejobs_tribute.txt'
file_handle = codecs.open(output_file,'w','utf-8')

# helper function to remove tabs and linefeeds
def clean(txt):
  return txt.replace('\n',' ').replace('\t',' ')

for i in range(0, message_range):
  req = url % i
  data = urllib2.urlopen(req).read()
  data = json.loads(data)
  file_handle.write(clean(data['mainText']) + '\n')
file_handle.close()
