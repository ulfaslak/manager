from twitter_manager import *
#sleep(randrange(1500))


def pop_old_friends():

	with open('recently_followed.csv', 'r') as in_file:
		recently_followed = []
		for line in in_file:
			recently_followed.append(int(line))

        count = len(recently_followed)/20

	old_friends = recently_followed[:count]
	del recently_followed[:count]


	with open('recently_followed.csv', 'w') as out_file:
		for _id in recently_followed:
			out_file.write(str(_id) + "\n")


	return old_friends



def destroy_old_friendships(old_friends):

	for _id in old_friends:
                try:
		    print "unfollowed %d" % _id
		    t.friendships.destroy(user_id=_id)
                except:
                    print "%d not found" % _id



def get_current_followers():

	return list(set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"]))



def get_followbacks(current_followers, old_friends):

	followbacks 		= []

	for friend in old_friends:
		if friend in current_followers:
			followbacks.append(friend)


	return followbacks



def get_assholes(current_followers, old_friends):

	assholes 			= []

	for friend in old_friends:
		if not friend in current_followers:
			assholes.append(friend)


	return assholes



def update_followbacks(followbacks):

	try:
		with open('followbacks.csv', 'r') as in_file:
			for line in in_file:
				followbacks.append(int(line))

	except IOError: # Type NameError May have to be changed
			pass


	with open('followbacks.csv', 'w') as out_file:
		for _id in followbacks:
			out_file.write(str(_id) + '\n')



def update_assholes(assholes):

	try:
		with open('assholes.csv', 'r') as in_file:
			for line in in_file:
				assholes.append(int(line))

	except IOError: # Type NameError May have to be changed
			pass


	with open('assholes.csv', 'w') as out_file:
		for _id in assholes:
			out_file.write(str(_id) + '\n')



def update_recently_followed(user_ids):
	recently_followed = []
	try:
		with open('recently_followed.csv', 'r') as in_file:
			for line in in_file:
				recently_followed.append(int(line))

	except IOError: # Type NameError May have to be changed
			pass


	for _id in user_ids:
		recently_followed.append(_id)


	with open('recently_followed.csv', 'w') as out_file:
		for _id in recently_followed:
			out_file.write(str(_id) + '\n')


# For testing

def get_current_friends():

	return list(set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"]))



# Load 200 oldest friends' ids in varaible and destroy friendships. Load all
# current followers here because it will be used twice in the following.

OLD_FRIENDS 		= pop_old_friends()
CURRENT_FOLLOWERS 	= get_current_followers()

OLD_NON_FOLLOWERS	= list(set(OLD_FRIENDS) - set(CURRENT_FOLLOWERS))

destroy_old_friendships(old_friends=OLD_NON_FOLLOWERS)



# Identify followbacks and store

FOLLOWBACKS		= list(set(OLD_FRIENDS) & set(CURRENT_FOLLOWERS))

update_followbacks(followbacks=FOLLOWBACKS)
update_recently_followed(user_ids=FOLLOWBACKS)



# Identify assholes and store ids

update_assholes(assholes=OLD_NON_FOLLOWERS)
