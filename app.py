from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request
from flask_jwt_extended import create_access_token
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_jwt_extended.utils import get_jwt_identity
import requests
import urllib.parse
import hmac
import hashlib
import base64

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
app.config['JWT_ALGORITHM'] = 'HS256'  # Use HS256 algorithm for JWT tokens
jwt = JWTManager(app)

def verify_jwt_token():
    try:
        verify_jwt_in_request()
        return True
    except JWTDecodeError:
        return False

@app.route('/login', methods=['POST'])
def login():
    # Perform authentication logic here
    username = request.json.get('username')
    password = request.json.get('password')
    

    # Example validation - replace with your actual authentication logic
    if username == 'admin' and password == 'password':
        # Generate JWT token
        access_token = create_access_token(identity=username)
        print(access_token)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    

@app.route('/pesapal', methods=['GET'])
@jwt_required()
def get_pesapal_iframe_url():
    if not verify_jwt_token():
        return jsonify({'message': 'Invalid token'}), 401
    
    pesapal_url = 'https://www.pesapal.com/api/PostPesapalDirectOrderV4'
    callback_url = 'http://www.test.com/redirect.php'  # Update with your redirect URL
    amount = '10.00'  # Sample amount
    desc = 'Test Payment'  # Sample description
    type = 'MERCHANT'  # Sample type
    reference = '123456'  # Sample reference
    first_name = 'Denis'  # Sample first name
    last_name = 'Karani'  # Sample last name
    email = 'karaniwdenis@gmail.com'  # Sample email
    phonenumber = ''

    consumer_key = app.config['PESAPAL_CONSUMER_KEY']
    print(consumer_key)
    consumer_secret = app.config['PESAPAL_CONSUMER_SECRET']
    print(consumer_secret)
    signature_method = 'HMAC-SHA1'

    post_xml = f"""<?xml version="1.0" encoding="utf8"?>
    <PesapalDirectOrderInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    Amount="{amount}" Description="{desc}" Type="{type}"
    Reference="{reference}" FirstName="{first_name}"
    LastName="{last_name}" Email="{email}"
    PhoneNumber="{phonenumber}" xmlns="http://www.pesapal.com" />"""
    post_xml = urllib.parse.quote(post_xml)

    from datetime import datetime
    import time
    timestamp = int(datetime.timestamp(datetime.now()))
    # print(timestamp)
    params = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': str(int(time.time())),  # Update with a unique value for each request
        'oauth_signature_method': signature_method,
        'oauth_timestamp': str(timestamp),  # Update with current timestamp
        'oauth_version': '1.0',
        'oauth_callback': callback_url,
        'pesapal_request_data': post_xml
    }

    encoded_params = urllib.parse.urlencode(sorted(params.items()))
    message = '&'.join(['GET', urllib.parse.quote(pesapal_url, safe=''), encoded_params])
    key = f"{consumer_secret}&"

    signature = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha1)
    signature_base64 = base64.b64encode(signature.digest())
    print(signature_base64.decode())
    params['oauth_signature'] = signature_base64.decode('utf-8')
    
    # Make a request to the Pesapal API to get the iframe URL
    response = requests.get(pesapal_url, params=params)
    if response.status_code == 200:
        iframe_url = response.text
        print(iframe_url)
        return jsonify({'iframe_url': iframe_url}), 200
    else:
        return jsonify({'message': 'Failed to retrieve iframe URL'}), 500
    
if __name__ == '__main__':
    app.run(port='5000', debug=True)