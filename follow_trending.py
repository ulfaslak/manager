from twitter_manager import *

sleep(randrange(1199))
print "Script: follow_trending.py"

# Terminal output

keyword = trending_topics()[randrange(10)]
print "\nSearching for users to follow in keyword: %s" % keyword
auto_follow(keyword, count=10)
