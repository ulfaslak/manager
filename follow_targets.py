from twitter_manager import *
import requests as rq

data = rq.get('http://ec2-54-77-226-94.eu-west-1.compute.amazonaws.com/static/targets').text
targets = [ int(n) for n in data.split('\n')[:-1] ]
friends = t.friends.ids(user_id=2749655899)['ids']

for userid in targets:
	if userid not in friends:
		t.friendships.create(user_id=userid, follow=True)
		write_user_to_current_friends(userid)
		write_user_to_already_followed(userid)

