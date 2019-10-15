from blogsley import db
from blogsley.models.users import User
from blogsley.models.blog import Post

users = User.query.all()
for u in users:
  db.session.delete(u)
posts = Post.query.all()
for p in posts:
  db.session.delete(p)
db.session.commit()