from flask.json import jsonify
import keys_management
import crypto
import twitter_management
import twitter_management_funcs
from flask import Flask, request, render_template
from twython import Twython
import os
from dotenv import load_dotenv

load_dotenv()


APP_KEY="IXDLY6HuNGXfw5DHeEOAAr3Tz"
APP_SECRET="4fYM0MPuspuNnKjUhYbdCe2GD5wfTnfREuuVmZ6kNaxfST17C6"
OAUTH_TOKEN="1123348351846625280-G6YN9t9yuJaKcvBIekhdEpBooVLixq"
OAUTH_TOKEN_SECRET="8TemMbe5Z1hsmkjApjy3wmYUB6CqbeIoriaqjBypi0ocd"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

app = Flask(__name__)

@app.route('/')
def landing():
    return (render_template("index.html"))

@app.route('/p1')
def p1():
    return (render_template("send_tweet.html"))

@app.route('/p2')  
def p2():
    return (render_template("receive_tweet.html"))

@app.route('/p3')
def p3():
    return (render_template("generate_keys.html"))

@app.route('/p4')
def p4():
    return (render_template("get_tweets.html"))


@app.route('/send', methods=['POST'])
def send():
    tweet = request.json["tweet"]
    user = request.json["user"]
    key = twitter_management.get_key_from_user(twitter, user)
    
    if key:
        encrypted_tweet = crypto.encrypt(bytes(tweet, encoding='utf8'), keys_management.convert_to_key(key))
        encrypted_tweet = twitter_management_funcs.encode_tweet(encrypted_tweet)
        encrypted_tweet = "#Encrypted\n" + encrypted_tweet
        twitter_management.post(twitter, encrypted_tweet)
        return 'Tweet realizado'
    else:
        return 'No tiene public key'

@app.route('/receive', methods=['GET'])
def receive():
    user = request.json["user"]
    private_key = keys_management.read_key("private_key.pem")
    tweets = twitter_management.get_tweets_from_user(twitter, user, private_key)
    return jsonify(tweets)

@app.route('/generate', methods=['GET'])
def generate():
    keys_management.generate_keys()
    public_key = keys_management.read_key("private_key.pem").public_key()
    public_key = keys_management.convert_to_string(public_key)
    public_key = "#PubKey\n" + public_key
    twitter_management.post(twitter, public_key) # Esta linea public la public key en el perfil
    
    return (render_template("generate_keys_success.html"))

@app.route('/get-tweets', methods=['GET'])
def get_tweets():
    private_key = keys_management.read_key("private_key.pem")
    tweets = twitter_management.get_tweets(twitter, private_key)
    return jsonify(tweets)

app.run(host='localhost', port=8080, debug=True)
