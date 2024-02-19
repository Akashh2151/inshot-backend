from mongoengine import Document, StringField, EmailField,DictField,ListField,DynamicField
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect 
from pydantic import ValidationError
from wtforms import URLField


# ziYpzvP0QHPnuCws
# akashh1
app = Flask(__name__)

# app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {
#     'db': 'authservice',
#     'host': 'mongodb+srv://akash1:ziYpzvP0QHPnuCws@cluster0.sl3hsc9.mongodb.net/?retryWrites=true&w=majority'
# }

# db = MongoEngine(app)
connect(db='authservice', host='mongodb+srv://akash1:ziYpzvP0QHPnuCws@cluster0.sl3hsc9.mongodb.net/authservice?retryWrites=true&w=majority')


def validate_non_empty(value):
    if isinstance(value, (str,)):
        if not value.strip():
            raise ValidationError("Field cannot be empty.")
    elif isinstance(value, (int, float)):
        # You can customize this part based on your requirements for numeric fields
        pass

# Define the User model
class User(Document):
    name = StringField(max_length=24)
    mobile = StringField(required=True, max_length=10, unique=True)  # Unique mobile field
    email = EmailField(unique=True, required=True)  # Unique email field
    password = StringField(required=True, max_length=100)
    # businessName = StringField(max_length=24)
    # businessMobile = StringField(max_length=10, unique=True)  # Unique businessMobile field
    # businessEmail = EmailField(unique=True, required=True)  # Unique businessEmail field
    # businessAddress = StringField(max_length=100)
    businessType = StringField(max_length=100)
    confirmPassword=StringField(required=True, max_length=100)
    # bundle = ListField(DynamicField())
    profilePic = StringField(required=False, null=True)
    
    
