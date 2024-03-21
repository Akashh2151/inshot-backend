from functools import wraps
import hashlib
from datetime import datetime, timedelta
import json
import re
import uuid
import bcrypt
from bson import ObjectId
from flask import Blueprint, app, current_app, request, jsonify
from flask_jwt_extended import jwt_required
import jwt
 
 
from model.signInsignup_model import  User
 
from security.allSecurity import email_regex,password_regex,phone_number
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
signUp_bp = Blueprint('signUp', __name__)
 


@signUp_bp.route('/v1/register', methods=['POST'])
def register_step1():
    try:
        data = request.json
        name = data.get('name')
        mobile = data.get('mobile')
        email = data.get('email')
        password = data.get('password')
        # confirmPassword=data.get('confirmPassword')
        # print(data)

        # Check if the email or mobile is already registered
        if User.objects(email=email).first() or User.objects(mobile=mobile).first():
            response = {"body": {}, "status": "error", "statusCode": 409, "message": 'Email or mobile is already registered'}
            return jsonify(response),200
        
        # if password != confirmPassword:
        #     response = {"body": {}, "status": "error", "statusCode": 400, "message": 'Password and confirm password do not match'}
        #     return jsonify(response),200

        # Validate required fields
        required_fields = [name, email, password, mobile]
        if not all(required_fields):
            response = {"body": {}, "status": "error", "statusCode": 400, "message": 'All required fields must be provided'}
            return jsonify(response), 200
        
        # Validate password and email format
        if not re.match(password_regex, password):
            response = {'body':  {}, 'status': 'error', 'statusCode': 422, 'message': 'Password must be at least 8 to 16 characters long'}
            return jsonify(response),200

        if not re.match(email_regex, email):
            response = {'body':  {}, 'status': 'error', 'statusCode': 422, 'message': 'Email requirement not met'}
            return jsonify(response),200
        
        if not re.match(phone_number,mobile):
            response = {'body': {}, 'status': 'error', 'statusCode': 422, 'message': 'Mobile number must be exactly 10 digits long and should only contain numeric characters.'}
            return jsonify(response),200
 
        # Hash the password
        userpassword = hashlib.sha256(password.encode()).hexdigest()

        # Create the User object
        user = User(
            name=name,
            mobile=mobile,
            email=email,
            password=userpassword,
            # confirmPassword=confirmPassword,
            userType="consumer", 
            profilePic=None
        )

        # Save the user to the database
        user.save()

        response = {"body": {}, "status": "success", "statusCode": 201, "message": 'Registration successfully'}
        return jsonify(response), 200

    except Exception as e:
        response = {"body": {}, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500


 
    
# ____________________________________________________________________________________________________________
# all working 
# @signUp_bp.route('/register/step1', methods=['POST'])
# def register_step1():
#     try:
#         data = request.json
#         userName = data.get('userName')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')
        
#         userpassword=hashlib.sha256(password.encode()).hexdigest()

 
#         # Check if the email is already registered
#         if User.objects(email=email).first():
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email is already registered'}
#             return jsonify(response), 400
        
            
#         if not userName or not email or not password or not role:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, email, password, and role are required'}
#             return jsonify(response), 400
        
#         # Define your password requirements
#         if not re.match(password_regex, password):
#             response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Password requirements not met'}
#             return jsonify(response)
        
#         # Define your email requirements
#         if not re.match(email_regex,email):
#                 response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Email requirement not met'}
#                 return jsonify(response)
        
#         user = User(
#             userName=userName,
#             email=email,
#             password=userpassword,
#             role=role,
#         )

#         # Save the user to the database
#         user.save()

#         # Retrieve the user ID after saving to the database and convert to string
#         user_id = str(user.id)      

#         # Include user ID in the response
#         response = {"Body": {"user_id": user_id}, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500


# @signUp_bp.route('/register/step2', methods=['POST'])
# def register_step2():
#     try:
#         data = request.json
#         name = data.get('name')
#         mobileNumber = data.get('mobileNumber')
#         businessName = data.get('businessName')
#         businessType = data.get('businessType')

#         if not name or not mobileNumber or not businessName or not businessType:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, name, mobile number, business name, and business type are required'}
#             return jsonify(response), 400

#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Update the user with additional information
#         user.name = name
#         user.mobileNumber = mobileNumber
#         user.businessName = businessName
#         user.businessType = businessType
      
        

#         # Perform additional validation if needed
#         if businessType == "resto" or businessType == "shop":
#             # Remove existing bundles if present
#             # Remove existing bundles if present
#             user.shopBundle = []
#             user.Bundle = []

#             if businessType == "shop":
#                 user.shopBundle = shop_data
#                 response = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#             elif businessType == "resto":
#                 user.Bundle = [resto_data]  # Wrap resto_data in a list
#                 response = jwt.encode({'bundle': resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#         # Save the updated user to the database
#         user.save()
        
#         response = {"Body": response, "status": "success", "statusCode": 200, "message": 'Step 2 successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
# ___________________________________________________________________________________________________________________
 



# @login_bp.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')
#         businessType = data.get('businessType')

#         # Validate the presence of 'email', 'password', and 'businessType'
#         if email is None or password is None or businessType is None:
#             return jsonify({'error': 'Email, password, and businessType are required', 'status_code': 400}), 400

#         # Find the user by email
#         user = User.objects(email=email).first()

#         if user:
#             # Check if the provided businessType matches the user's businessType
#             if user.businessType == businessType:
#                 provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
#                 # userpassword=hashlib.sha256(password.encode()).hexdigest()
#                 print(user.password)
#                 if provided_password_hash == user.password:
#                     payload = {
#                         'userId': str(user.id),
#                         'sub': '1',
#                         'jti': str(uuid.uuid4()),
#                         'identity': user.email,
#                         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
#                         'role': user.role,
#                         'type': 'access',
#                         'fresh': True
#                     }
#                     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256') 

#                     # Include user businessType in the response body based on its value
#                     if user.businessType == 'resto':
#                         encoded_resto_data = jwt.encode({'bundle':resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#                         return jsonify({'Body': encoded_resto_data,
#                                         'message': 'Login successful', 'access_token': token, 'status_code': 200})
#                     elif user.businessType == 'shop':
#                         encoded_shop_data = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#                         return jsonify({'Body': encoded_shop_data,
#                                         'message': 'Login successful', 'access_token': token, 'status_code': 200})
#                 else:
#                     return jsonify({'error':'password is Wrong'}), 401
#             else:
#                 return jsonify({'error': 'Invalid businessType'}), 401

#         return jsonify({'error': 'Invalid email or password'}), 401

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# Example configuration line
# VALID_API_KEY = "9f8b47de-5c1a-4a6b-8d92-d67c43f7a6c4"


# def require_api_key(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # Attempt to extract the token from the Authorization header
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             # Expecting header value in the format "Bearer <API_KEY>"
#             parts = auth_header.split()
#             if len(parts) == 2 and parts[0].lower() == 'bearer':
#                 api_key = parts[1]
#                 # Validate the API key
#                 if api_key == current_app.config['VALID_API_KEY']:
#                     return f(*args, **kwargs)
#         # If extraction fails or API key is invalid, return an error response
#         return jsonify({'message': 'Invalid or missing API Key', 'status': 'error', 'statusCode': 401}), 401
#     return decorated_function

EXPECTED_ENCRYPTION_KEY = "9f8b47de-5c1a-4a6b-8d92-d67c43f7a6c4"


# # login route
login_bp = Blueprint('login', __name__)
@login_bp.route('/v1/login', methods=['POST'])
# @require_api_key
def login():
   # Extracting the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.lower().startswith('bearer'):
        # The request contains a Bearer token, attempt to decode it
        token = auth_header[7:]
        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            return jsonify({'body':{},'decoded_token': decoded, 'message': "Token decoded successfully", "status": "success", "statusCode": 200}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'body':{},'message': "The token is expired", "status": "error", "statusCode": 401}), 200
        except jwt.InvalidTokenError:
            return jsonify({'body':{},'message': "Invalid token", "status": "error", "statusCode": 401}), 200
        except Exception as e:
            return jsonify({'body':{},'message': str(e),'status': 'error','statusCode': 500}), 500
        
     # Extract the custom encryption key from the request headers
    encryption_key = request.headers.get('X-Custom-Encryption-Key')

    # Verify the encryption key
    if encryption_key != EXPECTED_ENCRYPTION_KEY:
        return jsonify({'body':{},'message': "Invalid or missing encryption key", "status": "error", "statusCode": 401}), 200

    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return jsonify({'body':{},'message': 'Email and password are required', 'status': 'error', 'statusCode': 400}), 200

        # Replace this with your actual database lookup
        user = User.objects(email=email).first()

        if user:
            provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
            if provided_password_hash == user.password:
                # Set short expiration for the token
                exp_time = datetime.utcnow() + timedelta(minutes=1)
                payload = {
                            'sub': '1',
                            'jti': str(uuid.uuid4()),
                            'userId': str(user.id),
                            'exp':  exp_time,
                            'type': 'access',
                            'fresh': True
                }

                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

                userinfo={
                       "name":user.name,
                        "mobile":user.mobile,   
                        'identity': user.email
                }

                return jsonify({
                    "body": userinfo,
                    'message': 'Login successfully',
                    'status': 'success',
                    'accessToken': token,
                    'expires': exp_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'statusCode': 200
                }), 200
            else:
                return jsonify({'body':{},'message': 'Incorrect password', 'status': 'error', 'statusCode': 401}), 200
        else:
            return jsonify({'body':{},'message': 'User not found', 'status': 'error', 'statusCode': 404}), 200

    except Exception as e:
        return jsonify({'body':{},'message': str(e),'status': 'error','statusCode': 500}), 500
 
 

        
    
# @login_bp.route('/protected', methods=['GET'])
# @jwt_required
# def role_login():
#     try:
#         token = request.headers.get('Authorization').split()[1]
#         decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

#         user_role = decoded_token.get('role')

#         if user_role == 'admin':
#             return jsonify({'statusCode': 200, 'message': 'success', 'role': 'admin'}), 200
#         elif user_role == 'user':
#             return jsonify({'statusCode': 200, 'message': 'success', 'role': 'user'}), 200
#         else:
#             return jsonify({'statusCode': 403, 'message': 'Permission denied'}), 403
#     except UnicodeDecodeError as e:
#         # Handle the specific error when the token payload cannot be decoded
#         return jsonify({'statusCode': 400, 'error': 'Invalid token payload'}), 400
#     except Exception as e:
#         return jsonify({'statusCode': 500, 'error': str(e)}), 500
 
