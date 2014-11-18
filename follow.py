from twitter_manager import *

print "Script: follow.py"

# Keyword to search for users with
hashtag_bag = """#fitness #fitlife #nevergiveup #fitfam #healthy #wellness 
#fitblr #fitnessmotivation #inspiration #workoutmotivation #training #fitspo #fit
#fitspiration #workhard #trainhard #inshape #endurance #healthyliving #eatclean
""".split()

shuffle(hashtag_bag)

keyword = hashtag_bag[0]

sleep(randrange(540))
# Terminal output
print "\nSearching for users to follow in keyword: %s" % keyword
auto_follow(trending_topics(), count=15)
