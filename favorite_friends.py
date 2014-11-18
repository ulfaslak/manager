from twitter_manager import *


def fav_friends(n=10):
    """Favorite tweets from friends at random."""
    
    for i in range(n):
        
        following = t.friends.ids(screen_name=TWITTER_HANDLE)["ids"]
        shuffle(following)
        print "user_id:", following[0]
        tweets_list = t.statuses.user_timeline(_id=following[0])
       
        try:
            for tweet in tweets_list:
                if tweet['in_reply_to_status_id'] == None and not 'RT' in tweet['text']:
                    t.favorites.create(_id=tweet['id'])
                    print("favorited: %s" % (tweet["text"].encode("utf-8")))
                    break

        # when you have already favorited a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

det = randrange(2)
if det == 1:
    sleep(randrange(1500))
    fav_friends(2)
