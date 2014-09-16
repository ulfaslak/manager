import twitter
import twitter_manager as tm

# STRATEGY:	1. Mine twitter for people tweeting about trending subjects
#			2. Find users with minimum 2/3 following/followers ratio and follow
#			3. Follow 100 pr. day
#			4. Unfollow those who does not follow back in 24 hours

#### 1. Mine twitter for people tweeting about trending subjects

tm.auto_follow_followers()
tm.auto_unfollow_nonfollowers()