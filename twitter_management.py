from twython import Twython, TwythonError
import base64
import twitter_management
import crypto

def post(twitter, status):
    twitter.update_status(status=status)

def get_key_from_user(twitter, user):
    try:
        user_timeline = twitter.get_user_timeline(screen_name=user, tweet_mode='extended')
    except TwythonError as e:
        print(e)

    for tweets in user_timeline:
        for hashtags in tweets['entities']['hashtags']:
            if hashtags['text'] == 'PubKey':
                return parse_text(tweets['full_text'], 7)
    
    return None

def parse_text(key, n):
    parsed_key = ''
    for i in range(len(key)):
        if i > n: # skip #Pubkey
            parsed_key = parsed_key + key[i]
    return parsed_key

def encode_tweet(tweet):
    tweet = base64.b85encode(tweet)
    tweet = str(tweet)
    #             Tag people        random hashtag    random link
    tweet = tweet.replace('@', 'á').replace('#', 'é').replace('.', 'í')
    tweet = tweet[2:-1] # delete b''
    return tweet

def decode_tweet(tweet):
    #             Tag people        random hashtag    random link
    tweet = tweet.replace('á', '@').replace('é', '#').replace('í', '.').replace('&gt;','>').replace('&lt;','<').replace('amp;','')
    return tweet

def get_tweets_from_user(twitter, user, key):
    try:
        user_timeline = twitter.get_user_timeline(screen_name=user, tweet_mode='extended')
    except TwythonError as e:
        print(e)

    tweets = []

    for tweet in user_timeline:
        for hashtags in tweet['entities']['hashtags']:
            if hashtags['text'] == 'Encrypted':
                tweets.append(parse_text(tweet['full_text'], 10))

    decoded_tweets = []
    for tweet in tweets:
        decoded_tweets.append(twitter_management.decode_tweet(tweet))

    decrypted_tweets = []
    for tweet in decoded_tweets:
        tweet = base64.b85decode(tweet)
        decrypted_tweets.append(crypto.decrypt(tweet, key))

    return decrypted_tweets
