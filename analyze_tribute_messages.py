#!/usr/bin/python
#nltk.help.upenn_tagset('RB')
from collections import defaultdict
from operator import itemgetter
import re
import urllib2
import string
import simplejson as json

import codecs
import nltk


OUTPUT_FILE = 'data/stevejobs_tribute.txt'

adverbs = defaultdict(int)
adjectives = defaultdict(int)
bigrams = defaultdict(int)

message_has_adjective = False
message_has_adverb = False
message_contains_product_mention = False
messages_with_adjective = 0
messages_with_adverb = 0
messages = 0
messages_with_product_mention = 0

exclude = set(string.punctuation)

products = {'iPhone':{'regex':'iphones?','count':0},
	'iMac':{'regex':'imacs?','count':0},
	'iPad':{'regex':'ipads?','count':0},
	'iTunes':{'regex':'itunes','count':0},
	'iPod':{'regex':'ipods?','count':0},
	'cube':{'regex':'cubes?','count':0},
	'MacBook':{'regex':'macbooks?','count':0},
	'iBook':{'regex':'ibooks?','count':0},
	'Apple TV':{'regex':'apple ?tvs?','count':0},
	'Apple II Family':{'regex':r'(apple )?(2|ii|\]\[|\/\/)([ce\+|]|gs|s)?[^0-9]', 'count':0},
	'LaserWriter':{'regex':'laserwriter?','count':0},
	'PowerBook':{'regex':'powerbook?','count':0},
	'Newton':{'regex':'newton?','count':0},
	'OSX':{'regex':'osx','count':0},
	'iMovie':{'regex':'imovie','count':0},
	'Macintosh':{'regex':'macintosh','count':0},
	'Lisa':{'regex':'macintosh','count':0},
	'Mac':{'regex':'mac','count':0},
}

def top_n(dct,n = 10):
	srtd=sorted(dct.iteritems(), key=itemgetter(1), reverse=True)
	for x in srtd[0:n+1]:
		print x

def nltk_concordance(term,text_file):
	f = open(text_file).read()
	# remove punctuation
	f = f.translate(string.maketrans("",""), string.punctuation)
	split_text=nltk.Text(f.split())
	split_text.concordance(term,lines=100)

	# >>> f = f.translate(string.maketrans("",""), string.punctuation)
	# >>> foo=nltk.Text(f.split())
	# >>> print foo.concordance('newton')

	

def unescape(s):
	"""unescapes html codes"""
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&nbsp;", " ")
	# this has to be last:
	s = s.replace("&amp;", "&")
	return s


for line in open(OUTPUT_FILE):
	message_has_adjective = False
	message_has_adverb = False
	message_contains_product_mention = False
	
	# remove the trailing linefeed and convert to lower-case
	# and remove html control characters
	messages += 1
	data = line.strip()
	data = data.lower()
	data = unescape(data)
	
	# check for product mentions
	for k,v in products.iteritems():
		if re.search(v['regex'],data):
			products[k]['count'] += 1
			message_contains_product_mention = True
			
	# if the message contains a product mention
	# increment the product mention counter
	if message_contains_product_mention:
		messages_with_product_mention += 1


# tokenize the sentences using nltk's wordpuncttokenizer
	text = nltk.WordPunctTokenizer().tokenize(data) 

# compute trigrams
	nltk_trigrams = nltk.trigrams(text)
	for itm in nltk_trigrams:
		bigrams[itm] += 1

# pos-tag each token. we're interested in adjectives and adverbs
	parts_of_speech = nltk.pos_tag(text)
	# test for adjectives and adverbs, increment the counters
	# when we find one. 

	for (word,pos) in parts_of_speech:
		if pos.startswith('JJ'):
			message_has_adjective = True
			adjectives[word] += 1

		if pos.startswith('RB'):
			message_has_adverb = True
			adverbs[word] += 1

	# if the message contains an adverb or an adjective, increment a counter
	if message_has_adjective:
		messages_with_adjective += 1
	if message_has_adverb:
		messages_with_adverb += 1

n = 25
print "top %s adverbs" % n
top_n(adverbs, n)
print
print "top %s adjectives" % n
top_n(adjectives, n)

print "messages with adjectives: %s" % messages_with_adjective
print "messages with adverbs: %s" % messages_with_adverb
print "total messages with product mentions: %s" % messages_with_product_mention
print "total messages: %s" % messages


# n = 20
# print "top %s adjectives" % n
# top_n(bigrams, n)
srtd=sorted(products.iteritems(),key=itemgetter(1))
for x,y in srtd:
	print "%s\t\t%s" % (x,y['count'])
print
print
print "concordance for newton:"
nltk_concordance('newton',OUTPUT_FILE)