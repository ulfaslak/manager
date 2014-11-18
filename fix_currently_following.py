from twitter_manager import *

friends = t.friends.ids(user_id=2749655899)['ids']

with open('current_friends.csv','w') as out_file:
	for userid in friends:
		out_file.write(str(userid) + '\n')
