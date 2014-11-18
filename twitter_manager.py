from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import os
import io
import urllib
import json
import nltk
from urllib import urlopen
from random import randrange
from random import shuffle
from time import sleep
from StringIO import StringIO
from location_coordinates import *


# twitter tokens, keys, secrets, and Twitter handle in the following variables
CONSUMER_KEY = 'E19oBd9qdE1wXWiyixMfrubbI'
CONSUMER_SECRET ='IU5qiEwHJgKAVJN0fXMux79yIzsMISSjLORB3j8sXXvUFddlnV'
OAUTH_TOKEN = '2749655899-u4geaWEZHlCXtvk12wlVJ84JmSX4HIQuD3FEsDQ'
OAUTH_TOKEN_SECRET = 'NlUL020uY5mXW4nFonFI2PgWDMguv6V2aF9QGGQkCAly8'
TWITTER_HANDLE = "FitVeganGirl_"
TWITTER_ID = 2749655899

ALREADY_FOLLOWED_FILE = "already-followed.csv"
CURRENT_FRIENDS_FILE = "current_friends.csv"

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))
ts = TwitterStream(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))


def search_tweets(q, count=100, result_type="recent", lang='en', geocode="37.539991,-122.165501,48km"):
    """
        Returns a list of tweets matching a certain phrase (hashtag, word, etc.)
    """

    return t.search.tweets(q=q, result_type=result_type, count=count, lang=lang, geocode=geocode)



def write_user_to_current_friends(userid):
    with open('current_friends.csv', 'r') as infile:
        current_friends = []
        for line in infile:
            current_friends.append(int(line))

    current_friends.append(userid)

    with open('current_friends.csv', 'w') as outfile:
        for userid in current_friends:
            outfile.write(str(userid) + '\n')



def write_user_to_already_followed(userid):
    with open('already_followed.csv', 'r') as infile:
        already_followed = []
        for line in infile:
            already_followed.append(int(line))

    already_followed.append(userid)

    with open('already_followed.csv', 'w') as outfile:
        for userid in already_followed:
            outfile.write(str(userid) + '\n')




def auto_follow(q, count=20):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count)
    #print json.dumps(result,indent=1)
    friends_ = t.friends.ids(screen_name=TWITTER_HANDLE)["ids"]

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # read in the list of user IDs that the bot has already followed in the past
    do_not_follow = set()
    dnf_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            dnf_list.append(int(line))

    do_not_follow.update(set(dnf_list))
    del dnf_list

    print "Looking through %d tweet(s):\n" % count
#    for tweet in result['statuses']:
#        print tweet['text']
#    else:
#        print "\n"

    for tweet in result["statuses"]:
        print "---> Analysing user: %s" % tweet["user"]["screen_name"]
        if is_feasable(tweet) and is_likely_english(tweet) and is_SF(tweet):
            try:
                if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                        tweet["user"]["id"] not in friends_ and
                        tweet["user"]["id"] not in do_not_follow):

                    t.friendships.create(user_id=tweet["user"]["id"], follow=True)
                    
                    write_user_to_current_friends(tweet["user"]["id"])
                    write_user_to_already_followed(tweet["user"]["id"])

                    print("Followed      %s" % (tweet["user"]["screen_name"]))
                else:
                    print "New user      False"

            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))

                # quit on error unless it's because someone blocked me
                if "blocked" not in str(e).lower():
                    quit()
            print "\n"
        else:
            print "\n"
            continue



def auto_follow_followers():
    """
        Follows back everyone who's followed you
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=True)
        except Exception as e:
            print("error: %s" % (str(e)))


def auto_unfollow_nonfollowers():
    """
        Unfollows everyone who hasn't followed you back
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    users_keep_following = set([])

    not_following_back = following - followers

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # update the "already followed" file with users who didn't follow back
    already_followed = set(not_following_back)
    af_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            af_list.append(int(line))

    already_followed.update(set(af_list))
    del af_list

    with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")

    for user_id in not_following_back:
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print("unfollowed %d" % (user_id))



# -------------- HERE I CUSTOMIZE ----------------

def trending_topics():
    """
        Find trending topics to search for users with
    """

    #WORLD_WOE_ID = 1
    #US_WOE_ID = 23424977
    SF_WOE_ID = 2487956

    #world_trends =  t.trends.place(_id=WORLD_WOE_ID)
    #us_trends =     t.trends.place(_id=US_WOE_ID)
    sf_trends =     t.trends.place(_id=SF_WOE_ID)

    #world_trends_set =  set([trend['name'] for trend in world_trends[0]['trends']])
    #us_trends_set =     set([trend['name'] for trend in us_trends[0]['trends']])
    sf_trends_set =     set([trend['name'] for trend in sf_trends[0]['trends']])

    #common_trends_set = sf_trends_set.intersection(us_trends_set)
    #common_trends_list = list(common_trends_set)

    #q = common_trends_list[1]
    q = list(sf_trends_set)
    return q


def fol_fol_ratio(tweet):
    """
        Calculates the ratio between a users friends and followers
    """

    following = tweet['user']['friends_count']
    followers = tweet['user']['followers_count']
    return float(following)/followers


def is_feasable(tweet):
    """
        Returns true if a user is deemed likely to follow back
    """

    if fol_fol_ratio(tweet) > 2.0/3:
        print "Feasible      True"
        return True
    else:
        print "Feasible      False"
        return False


def is_likely_english(tweet):
    """
        Returns true if a tweet is likely english, otherwise false
    """

    common_en_words_str = """the be to of and a in that have it for not on
        with he as you do at this but his by from they we say her she or an
        will my one all would there their what so up out if about who get 
        which go me""" # top 50 common english words from wikitw

    #common_en_words_list = [(" " + word + " ") for word in common_en_words_str.split()]
    common_en_words_list = common_en_words_str.split()

    return_determinant = 0

    for word in common_en_words_list:
        if word in tweet['text']:
            return_determinant += 1
        else:
            continue

    if return_determinant > 5:
        print "English       True"
        return True
    
    print "English       False"
    return False


def is_SF(tweet):
    """
        Returns true if the tweet is geotagged, if there is SF in the user 
        description or in the user location.
    """
    SF_words = ['sf ', ' sf', 'san francisco', 'frisco', 'giants', 'bay area', 
                'silicon valley', 'the valley', 'san fran', 'sanfran']

    if tweet['coordinates'] != None:
        print "Coordinates   True"
        return True

    for word in SF_words:
        if word in tweet['user']['description'].lower():
            print "Description   True"
            return True
        elif word in tweet['user']['location'].lower():
            print "Location      True"
            return True

    print "From SF       False"
    return False


def tweet_is_tweeted(tweet):
    """
        Returns true of a tweet has already been tweeted
    """

    # Loads already tweeted tweets
    already_tweeted = t.statuses.user_timeline(screen_name=TWITTER_HANDLE)
    already_tweeted = [ntweet['text'] for ntweet in already_tweeted]
    
    return_type = False

    # Loops through tweeted tweets and sets return_type to True and breaks if it finds the tweet
    for ntweet in already_tweeted:
        if tweet in ntweet:
            return_type = True
            break

    return return_type



def post_from_reddit(subreddit):
    """
        Posts firstmost reddit content that fits in twitter format length.
    """

    # Storing html content of ..com/.json as string
    urlseek = 'http://www.reddit.com/r/' + subreddit + '/.json'
    html = urllib.urlopen(urlseek).read()

    # Converts html content to json format
    load = json.loads(html)

    # Loops through content to find posts of fitting length that hasn't been tweeted by me yet
    for i,_ in enumerate(load['data']['children']):
        if len(load['data']['children'][i]['data']['title']) < 117:
            if 'imgur' in load['data']['children'][i]['data']['url']:
                if not tweet_is_tweeted(load['data']['children'][i]['data']['title']):
                    title = load['data']['children'][i]['data']['title']
                    url = load['data']['children'][i]['data']['url']
                    update = str(title + " " + url)
                    t.statuses.update(status=update, lat=location_coordinates()[0], long=location_coordinates()[1])
                    break


def rt_popular():
    """
        Retweets a random tweet from a popular user
    """

    popular_bag = """FittyTips FoodHealth BeFitMotivation YourDailyVegan VegNews youcanbhealthy
    FIT_MOTIVATION FitspirationaI HeaIthTips Raw_Vegan veganfuture vegancook101 Fitness_Femme YesGlutenFree
    """

    popular_list = popular_bag.split()
    shuffle(popular_list)

    _id = t.statuses.user_timeline(screen_name=popular_list[0])[0]['id']
    t.statuses.retweet(id=_id)




#post_from_reddit('vegan')
#auto_follow('#fitspo')
