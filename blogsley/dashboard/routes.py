import os
import sys
from flask import render_template, request, current_app
from flask_login import current_user
from blogsley.dashboard import bp
from blogsley.dashboard.forms  import LoginForm, RegisterForm
from blogsley.models.blog import Post

@bp.route('/')
def index():
    return render_template('pages/index.html')

# Render the tables page
@bp.route('/posts.html')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(owner_id=current_user.id).order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('pages/posts.html', posts=posts.items)

@bp.route('/posts/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('pages/post-edit.html', post=post)

# Render the tables page
@bp.route('/tables.html')
def tables():
    return render_template('pages/tables.html')

# Render the icons page
@bp.route('/icons.html')
def icons():
    return render_template('pages/icons.html')

# Render the profile page
@bp.route('/profile.html')
def profile():
    return render_template('pages/profile.html')

# authenticate user
@bp.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))

# register user
@bp.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('dashboard.login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# authenticate user
@bp.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard.index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )
