from flask import Blueprint,render_template,request,flash,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# Hash function work
# x ->y
# f(x) = x + 1
# f(y) = y - 1
# f(2) -> 3
# f'(3) -> 2
# y -> x

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ["GET" , "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password! Try again!', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods = ["GET" , "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        user = User.query.filter_by(username = username).first()
        if user:
            flash('Username already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character', category = 'error')
        elif password != re_password:
            flash('Password doesnt match!', category = 'error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters', category = 'error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Sign up successed!', category = 'success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user = current_user)