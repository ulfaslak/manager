from twitter_manager import *

def get_oldest_friends(denominator):
	"Takes the top portion of the list of current friends"

	with open('current_friends.csv', 'r') as infile:
		friends = []
		for line in infile:
			friends.append(int(line))

	n = len(friends)/denominator
	oldest_friends = friends[:n]


	# Remove oldest_friends from friends, and write it back to current_friends
	
	friends = friends[n:]

	with open('current_friends.csv', 'w') as outfile:
		for userid in friends:
			outfile.write(str(userid) + '\n')


	return oldest_friends



def write_user_to_followbacks(userid):
	with open('followbacks.csv', 'r') as infile:
		followbacks = []
		for line in infile:
			followbacks.append(int(line))

	followbacks.append(userid)

	with open('followbacks.csv', 'w') as outfile:
		for userid in followbacks:
			outfile.write(str(userid) + '\n')



def write_user_to_assholes(userid):
	with open('assholes.csv', 'r') as infile:
		assholes = []
		for line in infile:
			assholes.append(int(line))

	assholes.append(userid)

	with open('assholes.csv', 'w') as outfile:
		for userid in assholes:
			outfile.write(str(userid) + '\n')



oldest_friends = get_oldest_friends(4)

followers_ = t.followers.ids(user_id=2749655899)['ids']


for userid in oldest_friends:


	if userid in followers_:
		write_user_to_followbacks(userid)
		print "Added user %d to followbacks." % userid

	else:
		write_user_to_assholes(userid)
		print "Added user %d to assholes." % userid


	t.friendships.destroy(user_id=userid)

print "Unfollowing users"




