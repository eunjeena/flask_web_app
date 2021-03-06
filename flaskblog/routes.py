from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")  # multi urls work same
def home():
    cur_page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        per_page=5, page=cur_page)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

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
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user and bcrypt.check_password_hash(exist_user.password,
                                                     form.password.data):
            # do log in
            login_user(exist_user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def save_picture(form_picture):
    '''save users picture to our File System by randomizing into hex'''
    import secrets
    random_hex = secrets.token_hex(8)

    import os  # os to grab file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)
    # resize picture before saving to save FS space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required  # enable users to access if logged in
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # if update image
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # post - get - redirect form
        # if we render_template, it reloads without saving
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static',  # directory
        filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required  # login required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',
                           title='New Post',
                           form=form,
                           legend='New Post')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)  # if doesn't exist, return 404
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # login required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only author can update
    if post.author != current_user:
        abort(403)  # http response forbidden route
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # when only updating, no need add()
        flash('Your post has been updated!', 'success')
        return redirect(url_for("posts.post", post_id=post.id))

    elif request.method == 'GET':
        # fill existing data
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@app.route("/user/<string:username>")
def user_posts(username):
    cur_page = request.args.get('page', 1, type=int)

    # if first is None, show 404
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.date_posted.desc())\
                      .paginate(page=cur_page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    # TODO
    token = user.get_reset_token()
    msg = Message('Password Reset Request for Cornercat',
                  sender='noreply@cornercat.com',
                  recipients=[user.email])  # recipients should be a list
    # _external=True: get absolute url (full domain)
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
    print('sent')


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # if already log-in, no need to reset
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been set with instructions to reset your password.',
            'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)  #return user obj, else None
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_reqeust'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pw  # no need to add, just update
        db.session.commit()

        flash('Your password has been updated! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form)
