from datetime import datetime
from slugify import slugify
from blogsley import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    filename = db.Column(db.String(100))
    src = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
