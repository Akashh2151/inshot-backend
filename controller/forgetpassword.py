import hashlib
import random
import re
import string
from flask import Blueprint, Flask, request, jsonify, session
from pymongo import MongoClient
# from model.forgetpassword_model import send_email
from model.signInsignup_model import User
from security.allSecurity import email_regex
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
forgetpassword_app = Blueprint('forgetpassword', __name__)
 
 

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp


def send_email(subject, recipient, message):
    try:
        sender_email = "akashdesai2151@gmail.com"
        sender_password = "okhnsnnviavjfsej"

        msg = MIMEText(message)
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email sending failed:", str(e))


@forgetpassword_app.route('/v1/sendotp', methods=['POST'])
def send_otp():
    try:
        user_id = request.headers.get('userId')
        email = request.json.get('email')

        if not user_id:
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 400,
                'message': 'UserID header is missing'
            }
            return jsonify(response), 200

        if not re.match(email_regex, email):
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 422,
                'message': 'Email format is invalid'
            }
            return jsonify(response), 200

        user = User.objects(id=user_id, email=email).first()
        if not user:
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 404,
                'message': 'The user ID entered does not correspond to an active user or email mismatch'
            }
            return jsonify(response), 200
        
        otp = ''.join(random.choices(string.digits, k=6))
        session['otp'] = otp
        message = f"Your OTP for password reset is: {otp}"
        send_email("Password Reset OTP", email, message)

        response = {
            'body': {},
            'status': 'success',
            'statusCode': 200,
            'message': 'OTP sent successfully'
        }
        return jsonify(response), 200

    except Exception as e:
        response = {
            'body': {},
            'status': 'error',
            'statusCode': 500,
            'message': f'An error occurred: {str(e)}'
        }
        return jsonify(response), 500
    


@forgetpassword_app.route('/v1/validateotp', methods=['POST'])
def validate_otp():
    try:
        entered_otp = request.json.get('otp')
        user_id = request.headers.get('userId')

        user = User.objects(id=user_id).first()
        if not user:
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 404,
                'message': 'The user ID entered does not correspond to an active user'
            }
            return jsonify(response), 200
        
        if 'otp' in session and session['otp'] == entered_otp:
            response = {
                'body': {},
                'status': 'success',
                'statusCode': 200,
                'message': 'OTP is valid'
            }
            return jsonify(response), 200
        else:
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 400,
                'message': 'Invalid OTP'
            }
            return jsonify(response),200
    except Exception as e:
        response = {
            'body': {},
            'status': 'error',
            'statusCode': 500,
            'message': f'An error occurred: {str(e)}'
        }
        return jsonify(response), 500




@forgetpassword_app.route('/v1/changepassword', methods=['PUT'])
def change_password():
    try:
        email = request.json.get('email')
        new_password = request.json.get('newPassword')
        confirm_password = request.json.get('confirmPassword')
        entered_otp = request.json.get('otp')
        user_id = request.headers.get('userId')


        user = User.objects(id=user_id, email=email).first()
        if not user:
            response = {
                'body': {},
                'message': 'The user ID entered does not correspond to an active user or email mismatch',
                'status': 'error',
                'statusCode': 404
                
            }
            return jsonify(response), 200
        

        if not re.match(email_regex, email):
            response = {
                'body': {},
                'message': 'Email format is invalid',
                'status': 'error',
                'statusCode': 422
                
            }
            return jsonify(response), 200
        

        if new_password != confirm_password:
            response = {"body": {}, "status": "error", "statuscode": 400, "message": 'Password and confirm password do not match'}
            return jsonify(response),200
        

        if 'otp' in session and session['otp'] == entered_otp:
            if new_password != confirm_password:
                session.pop('otp', None)  # Clear the OTP from session after use
                response = {
                    'body': {},
                    'status': 'error',
                    'statusCode': 400,
                    'message': 'Password and confirmation do not match'
                }
                return jsonify(response), 200
            
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            
            user = User.objects(email=email).first()
            if user:
                user.update(set__password=hashed_password)
                session.pop('otp', None)  # Clear the OTP from session after use
                response = {
                    'body': {},
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Password changed successfully'
                }
                return jsonify(response), 200
            else:
                response = {
                    'body': {},
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'User not found'
                }
                return jsonify(response), 200
        else:
            response = {
                'body': {},
                'status': 'error',
                'statusCode': 400,
                'message': 'Invalid OTP'
            }
            return jsonify(response), 200
    except Exception as e:
        response = {
            'body': {},
            'status': 'error',
            'statusCode': 500,
            'message': f'An error occurred: {str(e)}'
        }
        return jsonify(response), 500
