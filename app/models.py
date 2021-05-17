from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class MD_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT)
    body = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now().date())

    def __repr__(self):
        return '<Post {}>'.format(self.title)
