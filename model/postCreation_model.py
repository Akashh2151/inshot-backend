# from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField, IntField

import datetime
from mongoengine import Document, StringField, ReferenceField,DateTimeField,IntField,ListField
# from wtforms import DateTimeField
from model.signInsignup_model import User
# class User(Document):
#     name = StringField(required=True, max_length=120)
#     email = StringField(required=True)
#     password = StringField(required=True)  # For simplicity; in a real app, passwords should be hashed


class Post(Document):
    title = StringField(required=True)
    summary = StringField(required=True)
    post = StringField(required=True)  
    category = StringField(required=True)
    subCategory = ListField(StringField(), required=True)
    creator = ReferenceField(User, reverse_delete_rule=2)  
    likes = IntField(default=0)
    dislikes = IntField(default=0)
    shares = IntField(default=0)
    comment = IntField(default=0)
    viewCount = IntField(default=0)
    slug = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)


    

class CategoryMapping(Document):
    main_category = StringField(required=True)
    related_categories = ListField(StringField(required=True))

 
class Comment(Document):
    post = ReferenceField(Post, required=True)
    author = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Like(Document):
    post = ReferenceField(Post, required=True)
    user = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Dislike(Document):
    post = ReferenceField(Post, required=True)
    user = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Share(Document):
    post = ReferenceField(Post, required=True)
    user = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)


# class Reaction(Document):
#     post = ReferenceField(Post, required=True)
#     author = ReferenceField(User, required=True)
#     reaction_type = StringField(required=True)  # Could be 'like' or 'dislike'
#     created_at = DateTimeField(default=datetime.utcnow)
