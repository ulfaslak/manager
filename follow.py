from twitter_manager import *

print "Script: follow.py"
# Keyword to search for users with
keyword = '#fitspo'

sleep(randrange(540))
# Terminal output
print "\nSearching for users to follow in keyword: %s" % keyword
auto_follow(keyword)
