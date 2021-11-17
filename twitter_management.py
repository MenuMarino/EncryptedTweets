from twython import TwythonError
import base64
import crypto
import twitter_management_funcs

def post(twitter, status):
    twitter.update_status(status=status)

def get_key_from_user(twitter, user):
    try:
        user_timeline = twitter.get_user_timeline(screen_name=user, tweet_mode='extended')
    except TwythonError as e:
        print(e)

    pubkey = twitter_management_funcs.search_hashtag(user_timeline, 'PubKey')
    
    #print(twitter_management_funcs.clean_key(pubkey))
    if pubkey:
        return twitter_management_funcs.parse_text(pubkey[0], 7)
    else:
        return None

def get_tweets_from_user(twitter, user, key):
    try:
        user_timeline = twitter.get_user_timeline(screen_name=user, tweet_mode='extended')
    except TwythonError as e:
        print(e)

    tweets = twitter_management_funcs.search_hashtag(user_timeline, 'Encrypted')

    decoded_tweets = []
    for tweet in tweets:
        decoded_tweets.append(twitter_management_funcs.decode_tweet(tweet))

    decrypted_tweets = []
    for tweet in decoded_tweets:
        decrypted_tweets.append(crypto.decrypt(tweet, key))

    return decrypted_tweets

def get_tweets(twitter, key):
    timeline = twitter.get_home_timeline(tweet_mode='extended')
    tweets = twitter_management_funcs.search_hashtag(timeline, 'Encrypted')
    decoded_tweets = []
    for tweet in tweets:
        decoded_tweets.append(twitter_management_funcs.decode_tweet(tweet))

    decrypted_tweets = []
    for tweet in decoded_tweets:
        decrypted_tweets.append(crypto.decrypt(tweet, key))

    return decrypted_tweets
