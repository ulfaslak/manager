from twitter_manager import *

def favorite_mentions():
	mentions = t.statuses.mentions_timeline()

	mentions_list = [tweet['id'] for tweet in t.favorites.list(count=200)]

	for i in reversed(range(len(mentions))):
		if mentions[i]['id'] in mentions_list:
			continue
		else:
			try:
                                print "Attempting to favorite %s" % mentions[i]['text']
                        except:
                                print "Unicode Error but favoriting tweet anyway."
			t.favorites.create(_id=mentions[i]['id'])

sleep(randrange(3599))
favorite_mentions()
