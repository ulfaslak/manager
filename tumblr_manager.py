import pytumblr
import sys
from twitter_manager import *

tu = pytumblr.TumblrRestClient(
	'1e6SLA3EPSA6buqX7yeDYEMr0pACheY6d0SwSkGgvYjS4Gu5Tm',
	'dPX00RMbuosaxDSyWDs7RwELDoIT06C0FfQZtxbBZxWaCkotbd',
)

hashtag_bag = """#fitness #lifestyle #nutrition #motivation #fitfam #healthy #wellness 
#fitblr #fitnessmotivation #life #inspiration #workoutmotivation #training #firspo #fit
#fitspiration #workhard #trainhard #inshape #endurance
"""

hashtag_list = hashtag_bag.split()

def post_from_tumblr(user):
	"""
		Returns a twitter update composed of a tumblr picture and some hashtags.
	"""

	random = randrange(10)
	data = tu.posts(user)

	shuffle(hashtag_list)
	hashtags = hashtag_list[:randrange(3,6)]

	title = ' '.join(hashtags)
	url = data['posts'][random]['photos'][0]['original_size']['url']

	update = title + " " + url
	
	return update