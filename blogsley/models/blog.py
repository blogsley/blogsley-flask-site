from datetime import datetime
from slugify import slugify
from blogsley import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16))
    title = db.Column(db.String(256))
    slug = db.Column(db.String(256))
    model = db.Column(db.Text)
    cover = db.Column(db.String(256))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # tags

    def __init__(self, *args, **kwargs):
        
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))

        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        super(Post, self).__setattr__(key, value)
        if key == 'title':
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
