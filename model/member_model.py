import datetime
from mongoengine import Document, ReferenceField,DateTimeField
from model.postCreation_model import Post





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