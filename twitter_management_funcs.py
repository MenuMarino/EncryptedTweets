import base64

def parse_text(key, n):
    parsed_key = ''
    for i in range(len(key)):
        if i > n: # skip #Pubkey o #Encrypted
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
    tweet = base64.b85decode(tweet)
    return tweet

def search_hashtag(user_timeline, hashtag):
    tweets = []

    for tweet in user_timeline:
        for hashtags in tweet['entities']['hashtags']:
            if hashtags['text'] == hashtag:
                tweets.append(parse_text(tweet['full_text'], len(hashtag) + 1))

    return tweets

def clean_key(key):
    nkey = ''
    text = False
    for i in key:
        if(text):
            nkey = nkey + i
        if(i == '\n'):
            text = not text
    return key    

