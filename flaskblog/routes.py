from flask import Flask, render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        #msg, category(success, warning,error)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # name of function
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'ginana@test.com' and form.password.data == 'ginana':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)
