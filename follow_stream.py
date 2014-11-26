from twitter_manager import *

#sleep(randrange(3600))

# Collect users not to follow into a single list
friends_ = t.friends.ids(screen_name=TWITTER_HANDLE)["ids"]

already_followed = []
with open('already_followed.csv', 'r') as infile:
	for line in infile:
		already_followed.append(int(line))

do_not_follow = friends_ + already_followed + [TWITTER_ID]


# Get stream
stream = ts.statuses.filter(locations='-122.75,36.8,-121.75,37.8')


for i, tweet in enumerate(stream):
        print "--> User: %s" % tweet['user']['screen_name']
	if tweet['user']['id'] not in do_not_follow and is_feasable(tweet):
		t.friendships.create(user_id=tweet["user"]["id"], follow=True)
		print "Successfully followed user!"
		write_user_to_current_friends(tweet["user"]["id"])
		print "...wrote userid to current_friends.csv"
		write_user_to_already_followed(tweet["user"]["id"])
		print "...wrote userid to already_followed.csv"

        if i > 50:
            break
