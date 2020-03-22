from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# app protects against modifying cookies..
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '58c137a362f6cd22dabecdf4ecf42ca8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # can treate db structure as class (Model)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        '''how object is printed'''
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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


# to avoid these env settings:
# export FLASK_APP=<this file name>
# export FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)
