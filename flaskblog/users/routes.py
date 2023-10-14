from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email, send_confirm_email
from flask_login import login_user, current_user, logout_user, login_required
import os

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_confirm_email(user)
        flash(f"Account created for {form.username.data}! Confirm your email to log in","success")
        return redirect(url_for("users.login"))
    return render_template("register.html",title="Register",form=form)

@users.route("/confirm/<token>", methods=["GET","POST"])
def confirm_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token) 
    if user is None:
        flash("That is an invalid or expired token","warning")
        return redirect(url_for("users.login"))
    user.confirmed = True
    # make user admin if their email is in the list of admin emails
    if user.email == os.environ.get('EMAIL_USER'):
        user.is_admin = True
    db.session.commit()
    flash(f"Your email has been confirmed! You are now able to log in","success")
    return redirect(url_for("users.login"))

@users.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data) and user.confirmed:
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Login Successful!","success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        elif user and bcrypt.check_password_hash(user.password,form.password.data) and not user.confirmed:
            flash("Your account has not been confirmed yet. Please check your email for the confirmation link.","warning")
        else:
            flash("Login Unsuccessful. Please check email and password","danger")
    return render_template("login.html",title="Login",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) 
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash("Your account has been updated!","success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static",filename="profile_pics/"+current_user.image_file)
    return render_template("account.html",title="Account",image_file=image_file,form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page",1,type=int)
    user = User.query.filter_by(username=username).first_or_404() 
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=4, page=page)
    return render_template("user_posts.html",posts=posts,user=user)

@users.route("/reset_password", methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()   
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.","info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html",title="Reset Password",form=form)

@users.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token) 
    if user is None:
        flash("That is an invalid or expired token","warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password 
        db.session.commit()
        flash(f"Your password has been updated! You are now able to log in","success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html",title="Reset Password",form=form)

@users.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    # delete profile picture of current_user if it is not the default one
    prev_picture = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and current_user.image_file != "default.jpg":
        os.remove(prev_picture)
    # delete all the posts where the author is the current user
    posts = Post.query.filter_by(author=current_user).all()
    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted!","success")
    return redirect(url_for("main.home"))