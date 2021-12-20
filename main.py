<<<<<<< HEAD
from flask.json import jsonify
import keys_management
import crypto
import twitter_management
import twitter_management_funcs
from flask import Flask, request, render_template, redirect, url_for
from twython import Twython
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

APP_KEY="rfInTtyuJU3UHwGzOHIZl17UW"
APP_SECRET="a14MIZUFfHDmI9E26winqj2fF57ceD2XP6dE9JXw1ZBsDLPIuu"

app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

oauth.register(
    name='twitter',
    client_id=APP_KEY,
    client_secret=APP_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs=None,
)

@app.route('/')
def landing():
    return (render_template("index.html"))

@app.route('/login_session')
def login_sucess():
    return (render_template("login_session.html"))

@app.route('/login_session_keys')
def login_sucess_keys():
    return (render_template("login_session_keys.html"))

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

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    global OAUTH_TOKEN
    global OAUTH_TOKEN_SECRET
    global twitter

    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    resp.raise_for_status()
    OAUTH_TOKEN = token['oauth_token']
    OAUTH_TOKEN_SECRET = token['oauth_token_secret']
    print(OAUTH_TOKEN)
    print(OAUTH_TOKEN_SECRET)
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return redirect('/login_session')

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
        return jsonify('Tweet realizado')
    else:
        return jsonify('No tiene public key')

@app.route('/receive', methods=['POST'])
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

@app.route('/check-keys')
def check_keys():
    return jsonify(twitter_management.get_key(twitter))

app.run(host='localhost', port=8080, debug=True)
=======
from flask.json import jsonify
import keys_management
import crypto
import twitter_management
import twitter_management_funcs
from flask import Flask, request, render_template, redirect, url_for
from twython import Twython
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')

app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

oauth.register(
    name='twitter',
    client_id=APP_KEY,
    client_secret=APP_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs=None,
)

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

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    global OAUTH_TOKEN
    global OAUTH_TOKEN_SECRET
    global twitter

    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    resp.raise_for_status()
    OAUTH_TOKEN = token['oauth_token']
    OAUTH_TOKEN_SECRET = token['oauth_token_secret']
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return redirect('/')

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
>>>>>>> 6563e03c00effe1eaf43daa6fc7db12f521fab18
