from twitter_manager import *

print "Script: unfollow.py"
sleep(randrange(3600))
auto_follow_followers()
auto_unfollow_nonfollowers()
