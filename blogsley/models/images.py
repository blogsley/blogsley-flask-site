from datetime import datetime
from slugify import slugify
from blogsley import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
