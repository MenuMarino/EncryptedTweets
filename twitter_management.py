from twython import Twython

def post_key(twitter, key):
    twitter.update_status(status=key)
