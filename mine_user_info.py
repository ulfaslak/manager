from twitter_manager import *
from datetime import date


def get_word_scores():
    words = []
    scores = []
    with open('Data_Set_S1.txt', 'r') as in_file:
        for i, line in enumerate(in_file):
            if i >= 5:
                words.append(line.split('\t')[0])
                scores.append(line.split('\t')[2]) # 2: Happiness average, 3: happiness std

    word_scores = zip(words, scores)

    return word_scores


def get_stopwords():
    with open('stopwords.txt', 'r') as in_file:
        stopwords = in_file.read().split('\n')

    return stopwords


def friends_followers_reciprocals(userid):
    friends     = t.friends.ids(user_id=userid)
    followers   = t.followers.ids(user_id=userid)

    friends     = set(friends['ids'])
    followers   = set(followers['ids'])

    return friends, followers, list(friends & followers)[:50]


## --------------


def followers(user_profile):
    return user_profile['followers_count']


def friends(user_profile):
    return user_profile['friends_count']


def friends_to_followers_ratio(user_profile):

    friends = user_profile['friends_count']
    followers = user_profile['followers_count']

    return friends / float(followers)


def age(user_profile):

    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    raw_date = user_profile['created_at']
    
    year = int(raw_date[-4:])
    month = months[raw_date[4:7]]
    day = int(raw_date[8:10])

    d0 = date(year, month, day)

    return (date.today() - d0).days


def avg_hashtags_in_tweets(user_tweets):
    number_of_hashtags = []
    for tweet in user_tweets:
        number_of_hashtags.append(len(tweet['entities']['hashtags']))

    return sum(number_of_hashtags) / float(len(number_of_hashtags))


def avg_links_in_tweets(user_tweets):
    number_of_links = []
    for tweet in user_tweets:
        number_of_links.append(len(tweet['entities']['urls']))

    return sum(number_of_links) / float(len(number_of_links))


def avg_tweet_happiness(user_tweets):

    tweets      = [ tweet['text'] for tweet in user_tweets ]
    tok_tweets  = [ tweet.lower().split() for tweet in tweets ]
    stopwords   = get_stopwords()

    cl_tweets   = [ filter(lambda x: x not in stopwords, tok_tweet) 
                        for tok_tweet in tok_tweets ]

    scores = get_word_scores()
    values = []

    for tweet in cl_tweets:
        #print tweet
        for word in tweet:
            for hword, score in scores:
                if word in hword:
                    values.append(float(score))
                    #print "'" + hword + "'" + ' found'
                    break

    return sum(values) / float(len(values))



def reciprocal_friends_to_friends_ratio(user_profile):
    
    userid = user_profile['id']

    friends, _, reciprocals = friends_followers_reciprocals(userid)

    return  len(reciprocals) / float(len(friends))



def avg_reciprocal_friend_happiness(user_profile):

    user_id = user_profile['id']

    _, _, reciprocals = friends_followers_reciprocals(user_id)

    values = []
    for userid in reciprocals:
        try:
            user_tweets = t.statuses.user_timeline(user_id=userid, count=50)
        except: 
            print "...in avg_reciprocal_friend_happiness ---> couldn't retrieve tweets for %d, friend of %d." % (userid, user_id)
            continue
        try:
            avg_happiness = avg_tweet_happiness(user_tweets)
        except:
            print "...in avg_reciprocal_friend_happiness ---> couldn't calculate avg_happiness for %d, friend of %d." % (userid, user_id)
            continue
        values.append(avg_happiness)

    return sum(values) / float(len(values))



def avg_non_reciprocal_friend_happiness(user_profile):

    user_id = user_profile['id']

    friends, _, reciprocals = friends_followers_reciprocals(user_id)

    non_reciprocals = list(set(friends) - set(reciprocals))[:50]

    values = []
    for userid in non_reciprocals:
        try:
            user_tweets = t.statuses.user_timeline(user_id=userid, count=50)
        except:
            print "...in avg_non_reciprocal_friend_happiness ---> couldn't retrieve tweets for %d, friend of %d." % (userid, user_id)
            continue
        try:
            avg_happiness = avg_tweet_happiness(user_tweets)
        except:
            print "...in avg_non_reciprocal_friend_happiness ---> couldn't calculate avg_happiness for %d, friend of %d." % (userid, user_id)
            continue
        values.append(avg_happiness)

    return sum(values) / float(len(values))



def statuses_to_age_ratio(user_profile):
    
    statuses = user_profile['statuses_count']
    user_age = age(user_profile)

    return statuses / float(user_age)
    


def favorites_to_age_ratio(user_profile):

    favorites = user_profile['favourites_count']
    user_age = age(user_profile)

    return favorites / float(user_age)



def replies_to_statuses_ratio(user_tweets):

    replies = 0
    for tweet in user_tweets:
        if tweet['in_reply_to_status_id'] != None:
            replies += 1

    return replies / float(len(user_tweets))



def RTs_to_statuses_ratio(user_tweets):

    RTs = 0
    for tweet in user_tweets:
        if 'RT' in tweet['text']:
            RTs += 1

    return RTs / float(len(user_tweets))


def originals_to_statuses_ratio(user_tweets):

    originals = 0
    for tweet in user_tweets:
        if tweet['in_reply_to_status_id'] == None and 'RT' not in tweet['text']:
            originals += 1

    return originals / float(len(user_tweets))


def friends_following_me(user_profile):

    userid = user_profile['id']

    friends, _, _ = friends_followers_reciprocals(userid)
    _, followers, _ = friends_followers_reciprocals(2749655899) # FitVeganGirl_

    return len(list(set(friends) & set(followers)))



def write_featureset(userid):#,list):
    """Return feature array, X_i, and target, y_i, for a dataobject.
    """

    try:
        user_tweets = t.statuses.user_timeline(user_id=userid, count=50)
        print "\nSuccessfully retrieved user %d tweets." % userid
    except:
        return "Can't extract features for user %d, tweets not available." % userid

    user_profile = user_tweets[0]['user']

    X_i = []

    try:
        X_i.append(friends(user_profile))
        print "Successfully appended friends to featureset."
    except:
        print "Can't extract friends. Appending 0."
        X_i.append(0)

    try:
        X_i.append(followers(user_profile))
        print "Successfully appended followers to featureset."
    except:
        print "Can't extract followers. Appending 0."
        X_i.append(0)

    try:
        X_i.append(friends_to_followers_ratio(user_profile))
        print "Successfully appended friends_to_followers_ratio to featureset."
    except:
        print "Can't extract friends_to_followers_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(age(user_profile))
        print "Successfully appended age to featureset."
    except:
        print "Can't extract age. Appending 0."
        X_i.append(0)

    try:
        X_i.append(avg_hashtags_in_tweets(user_tweets))
        print "Successfully appended avg_hashtags_in_tweets to featureset."
    except:
        print "Can't extract avg_hashtags_in_tweets Appending 0."
        X_i.append(0)

    try:
        X_i.append(avg_links_in_tweets(user_tweets))
        print "Successfully appended avg_links_in_tweets to featureset."
    except:
        print "Can't extract avg_links_in_tweets. Appending 0."
        X_i.append(0)

    try:
        X_i.append(reciprocal_friends_to_friends_ratio(user_profile))
        print "Successfully appended reciprocal_friends_to_friends_ratio to featureset."
    except:
        print "Can't extract reciprocal_friends_to_friends_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(avg_tweet_happiness(user_tweets))
        print "Successfully appended avg_tweet_happiness to featureset."
    except:
        print "Can't extract avg_tweet_happiness. Appending 0."
        X_i.append(0)

        #X_i.append(avg_reciprocal_friend_happiness(user_profile)) # We know this is roughly the same as the users own happiness, no need including it
    try:
        X_i.append(avg_non_reciprocal_friend_happiness(user_profile))
        print "Successfully appended avg_non_reciprocal_friend_happiness to featureset."
    except:
        print "Can't extract avg_non_reciprocal_friend_happiness. Appending 0."
        X_i.append(0)

    try:
        X_i.append(statuses_to_age_ratio(user_profile))
        print "Successfully appended statuses_to_age_ratio to featureset."
    except:
        print "Can't extract --XX--. Appending 0."
        X_i.append(0)

    try:
        X_i.append(favorites_to_age_ratio(user_profile))
        print "Successfully appended favorites_to_age_ratio to featureset."
    except:
        print "Can't extract favorites_to_age_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(replies_to_statuses_ratio(user_tweets))
        print "Successfully appended replies_to_statuses_ratio to featureset."
    except:
        print "Can't extract replies_to_statuses_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(RTs_to_statuses_ratio(user_tweets))
        print "Successfully appended RTs_to_statuses_ratio to featureset."
    except:
        print "Can't extract RTs_to_statuses_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(originals_to_statuses_ratio(user_tweets))
        print "Successfully appended originals_to_statuses_ratio to featureset."
    except:
        print "Can't extract originals_to_statuses_ratio. Appending 0."
        X_i.append(0)

    try:
        X_i.append(friends_following_me(user_profile))
        print "Successfully appended friends_following_me to featureset."
    except:
        print "Can't extract friends_following_me. Appending 0."
        X_i.append(0)


    return X_i



















