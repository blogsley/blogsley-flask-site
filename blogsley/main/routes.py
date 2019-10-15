from flask import render_template, request, current_app
from flask_login import current_user, login_required, login_user, logout_user
from flask_babel import _
from blogsley.models.users import User
from blogsley.models.blog import Post
from blogsley.main.forms import EditProfileForm, PostForm, SearchForm, ContactForm
from blogsley.main import bp

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', posts=posts.items)

@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('blog.html', posts=posts.items)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('contact.html', title=_('Contact'), form=form)

@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(owner_id=user.id).order_by(Post.timestamp.desc())
    return render_template('user.html', user=user, posts=posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)

@bp.route('/posts/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)