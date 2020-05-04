from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _

from __blogsley__ import db
from blogsley_flask.jwt import encode_auth_token
from blogsley_flask.user import User

from blogsley_site.auth import bp
from blogsley_site.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from blogsley_site.auth.emails import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if '@' in email:
            user = User.query.filter_by(email=form.email.data).first()
        else:
            user = User.query.filter_by(username=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('root.index')
        return redirect(next_page)
    # return render_template('login.html', title=_('Log In'), form=form)
    return render_template('layouts/auth-default.html',
        content=render_template( 'pages/login.html', form=form ) )



@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data)
        user = User(username=form.email.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    # return render_template('register.html', title=_('Register'), form=form)
    return render_template('layouts/auth-default.html',
        content=render_template( 'pages/register.html', form=form ) )


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('root.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

@bp.route('/token', methods=['POST'])
def token():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = encode_auth_token(sub=username, id=user.id)
    print(access_token)
    return jsonify({"token": access_token.decode('utf-8')}), 200