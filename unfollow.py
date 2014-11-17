from twitter_manager import *

det = 1
if det == 1:
    print "Script: unfollow.py"
    sleep(randrange(3600))
    #auto_follow_followers()
    auto_unfollow_nonfollowers()
