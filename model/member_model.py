import datetime
from mongoengine import Document, ReferenceField,DateTimeField,StringField,IntField
from model.postCreation_model import Post
from model.signInsignup_model import User


class News(Document):
    title = StringField(required=True)
    summary = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    reference = StringField()
    # post = StringField(required=True)  
    category = StringField(required=True)
    subCategory = StringField(required=True)
    creator = ReferenceField(User, reverse_delete_rule=2)  
    likes = IntField(default=0)
    dislikes = IntField(default=0)
    shares = IntField(default=0)
    comments=  IntField(default=0)
    viewCount = IntField(default=0)
    validTill = DateTimeField()
    niche = StringField()
    created_At = DateTimeField(default=datetime.datetime.utcnow)


class Like(Document):
    post = ReferenceField(Post, required=True)
    # user = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Dislike(Document):
    post = ReferenceField(Post, required=True)
    # user = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Share(Document):
    post = ReferenceField(Post, required=True)
    # user = ReferenceField(required=True,null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)