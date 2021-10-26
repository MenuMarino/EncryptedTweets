import keys_management
import crypto
import twitter_management
from flask import Flask, request
from twython import Twython
import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv('APP_KEY') # Consumer key
APP_SECRET = os.getenv('APP_SECRET') # Consumer secret
OAUTH_TOKEN = os.getenv('AUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('AUTH_SECRET')
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

app = Flask(__name__)

@app.route('/')
def landing():
    return 'Encrypted Tweets.'

@app.route('/send', methods=['POST'])
def send():
    tweet = request.json["tweet"]
    user = request.json["user"]
    # key = keys_management.get_key_from_user(user)
    key = keys_management.read_key("private_key.pem")
    encrypted_tweet = crypto.encrypt(bytes(tweet, encoding='utf8'), key.public_key())
    return encrypted_tweet

@app.route('/receive', methods=['GET'])
def receive():
    return 'TODO'

@app.route('/generate', methods=['GET'])
def generate():
    keys_management.generate_keys()
    public_key = keys_management.read_key("private_key.pem").public_key()
    public_key = keys_management.convert_to_string(public_key)
    public_key = "#PubKey\n" + public_key
    twitter_management.post_key(twitter, public_key)
    return 'Keys generadas y public key twiteada'

app.run(host='localhost', port=8080, debug=True)
