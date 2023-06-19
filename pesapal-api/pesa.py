#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import jwt
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data

#         if username == 'admin' and password == 'pass123':
#             token = jwt.encode({'username': username}, app.config['SECRET_KEY'])
#             return redirect ('/get_iframe_url')
#             # return jsonify({'token': token})


#     return render_template('login.html', form=form)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    try:
        # Check if the credentials exist in the database
        username = User.query.filter_by(username=username).first()
        if username is not None and password == password:
            # Authentication successful
            token = jwt.encode({'username': username}, app.config['SECRET_KEY'])

        # Authentication failed
        return jsonify({'message': 'Invalid username or password'})

    except SQLAlchemyError as e:
        # Handle database errors
        return jsonify({'message': 'An error occurred while accessing the database'})

    # Form validation failed
    return jsonify({'message': 'Invalid form data'})

if __name__ == '__main__':
    app.run()

def get_token():

    url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    headers = {"Content-Type": "application/json"}

    payload = {
        "consumer_key": "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW",
        "consumer_secret": "osGQ364R49cXKeOYSpaOnT++rHs="
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    return data["token"]

# print(get_token())

def register_ipn_token():
    token = "Bearer {}".format(get_token())
    url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    payload = {
        "url": "https://www.myapplication.com/ipn",
        "ipn_notification_type": "GET"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()


    return data["ipn_id"]
@app.route('/get_iframe_url')
def get_iframe_url():

    token = "Bearer {}".format(get_token())
    generated_id = register_ipn_token()
    url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    payload = {
        "id": generated_id,
        "currency": "KES",
        "amount": 100.00,
        "description": "Payment description goes here",
        "callback_url": "https://www.myapplication.com/response-page",
        "notification_id": "fe078e53-78da-4a83-aa89-e7ded5c456e6",
        "billing_address": {
            "email_address": "",
            "phone_number": "",
            "country_code": "",
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "line_1": "",
            "line_2": "",
            "city": "",
            "state": "",
            "postal_code": '01000',
            "zip_code": '01000'
        }
        }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    return redirect(data['redirect_url'])
