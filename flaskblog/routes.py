from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'author': 'gina na',
    'title': 'Blog post 1',
    'content': 'First post content',
    'date_posted': 'April 20, 2018'
}, {
    'author': 'koji okayasu',
    'title': 'Blog post 2',
    'content': 'Second post content',
    'date_posted': 'April 21, 2018'
}]


@app.route("/")
@app.route("/home")  # multi urls work same
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('login'))  # name of function
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user and bcrypt.check_password_hash(exist_user.password,
                                                     form.password.data):
            # do log in
            login_user(exist_user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required  # enable users to access if logged in
def account():
    return render_template('account.html', title='Account')
