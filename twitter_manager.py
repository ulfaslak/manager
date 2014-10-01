"""
Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

from twitter import Twitter, OAuth, TwitterHTTPError
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
OAUTH_TOKEN = '2749655899-rBxZMaf3TSXnsrbhpRKm63ASU80BZpCrglobZKT'
OAUTH_TOKEN_SECRET = 'pqMgG4KSVS395DNJ6snYKvQNjxbQg1ggHyglFEOutvLTy'
TWITTER_HANDLE = "FitVeganGirl_"

# put the full path and file name of the file you want to store your "already followed"
# list in
ALREADY_FOLLOWED_FILE = "already-followed.csv"

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))


def search_tweets(q, count=100, result_type="recent"):
    """
        Returns a list of tweets matching a certain phrase (hashtag, word, etc.)
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def auto_fav(q, count=2, result_type="recent"):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        if is_feasable(tweet) and is_likely_english(tweet):
            try:
                # don't favorite your own tweets
                if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                    continue

                result = t.favorites.create(_id=tweet["id"])
                print("favorited: %s" % (result["text"].encode("utf-8")))

            # when you have already favorited a tweet, this error is thrown
            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))


def auto_rt(q, count=2, result_type="recent"):
    """
        Retweets tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        if is_feasable(tweet) and is_likely_english(tweet):
            try:
                # don't retweet your own tweets
                if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                    continue

                result = t.statuses.retweet(id=tweet["id"])
                print("retweeted: %s" % (result["text"].encode("utf-8")))

            # when you have already retweeted a tweet, this error is thrown
            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))


def auto_follow(q, count=10, result_type="recent"):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])

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

    print "Looking through the %d tweet(s):\n" % count
#    for tweet in result['statuses']:
#        print tweet['text']
#    else:
#        print "\n"

    for tweet in result["statuses"]:
        if is_feasable(tweet) and is_likely_english(tweet):
            try:
                if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                        tweet["user"]["id"] not in following and
                        tweet["user"]["id"] not in do_not_follow):

                    t.friendships.create(user_id=tweet["user"]["id"], follow=True)
                    following.update(set([tweet["user"]["id"]]))

                    print("followed %s" % (tweet["user"]["screen_name"]))

            except TwitterHTTPError as e:
                print("error: %s" % (str(e)))

                # quit on error unless it's because someone blocked me
                if "blocked" not in str(e).lower():
                    quit()
        else:
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

    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977

    world_trends =  t.trends.place(_id=WORLD_WOE_ID)
    us_trends =     t.trends.place(_id=US_WOE_ID)

    world_trends_set =  set([trend['name'] for trend in world_trends[0]['trends']])
    us_trends_set =     set([trend['name'] for trend in us_trends[0]['trends']])
    common_trends_set = world_trends_set.intersection(us_trends_set)
    common_trends_list = list(common_trends_set)

    q = common_trends_list[1]
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
        return True
    else:
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

    return_type = False
    return_determinant = 0

    for word in common_en_words_list:
        if word in tweet['text']:
            return_determinant += 1
        else:
            continue

    if return_determinant > 5:
        return_type = True

    return return_type


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


def fav_friends(n=10):
    """
        Randomly favorite tweets from friends
    """
    
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

#post_from_reddit('vegan')
