import keys_management
import crypto
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def landing():
    return 'Hello world'

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
    public_key = keys_management.read_key("private_key.pem")
    # Twitear la public key
    return 'Keys generadas'

app.run(host='localhost', port=8080, debug=True)
