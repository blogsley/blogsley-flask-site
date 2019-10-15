from blogsley import db
from blogsley.models.users import User
from blogsley.models.blog import Post

u = User(username='admin',
  first_name='The',
  last_name='Admin',
  email='admin@example.com',
  role='Admin',
  about_me='I am the Admin'
)
u.set_password('x')
db.session.add(u)
db.session.commit()

u = User(username='john',
  first_name='John',
  last_name='Doe',
  email='john@example.com',
  role='Editor',
  about_me='I am an Editor'
)
u.set_password('x')
db.session.add(u)
db.session.commit()

p = Post(
  title='Pugsley, a python user group webapp',
  summary='Pugsley is a webapp written in Python',
  body='Pugsley is a webapp written in Python',
  author=u
)
db.session.add(p)
db.session.commit()

u = User(
  username='susan',
  first_name='Susan',
  last_name='Smith',
  email='susan@example.com',
  role='Author',
  about_me='I am an Author'
)
u.set_password('x')
db.session.add(u)
db.session.commit()

p = Post(
  title='Python is cool!',
  summary='I love writing programs in Python',
  body='I love writing programs in Python',
  author=u
)
db.session.add(p)
db.session.commit()

u = User(
  username='joe',
  first_name='Joe',
  last_name='Jackson',
  email='joe@example.com',
  role='Reader',
  about_me='I am a Reader'
)
u.set_password('x')
db.session.add(u)
db.session.commit()

users = User.query.all()
print(users)

posts = Post.query.all()
for p in posts:
  print(p.id, p.author.username, p.body)