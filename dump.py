from blogsley import db
from blogsley.models.users import User
from blogsley.models.blog import Post

users = User.query.all()
print(users)

posts = Post.query.all()
for p in posts:
  print(p.id, p.author.username, p.body)