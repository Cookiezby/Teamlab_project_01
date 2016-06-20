from app import app, db, models
from flask import render_template, flash, redirect, g, request
from .forms import LoginForm, RegisterForm, PostForm, ProfileForm
from datetime import datetime
from flask.ext.login import login_user, logout_user, login_required, current_user
from t_service import PostService, UserService
import re

POST_PER_PAGE = 10


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated():
        return redirect('/posts')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_exist = models.User.query.filter_by(name=form.name.data).first()
        if user_exist:
            error_message = "UserName Already exist"
            return render_template('t_register.html', title='Register', form=form, error_message=error_message)
        elif form.pwd_confirm.data == form.password.data:
            flash('Register info username = %s, password = %s'
                  % (form.name.data, form.password.data))
            user = models.User(name=form.name.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/posts')
        else:
            error_message = "Please Check the Password"
            return render_template('t_register.html', title='Register', form=form, error_message=error_message)
    else:
        return render_template('t_register.html', title='Register', form=form)


@app.route('/posts', methods=['GET', 'POST'])
@app.route('/posts/<int:page>', methods=['GET', 'POST'])
@login_required
def posts(page=1):
    form = PostForm()
    usernames = []
    postbodies = []
    posts = PostService.get_user_followed_post(current_user.id, page, POST_PER_PAGE)
    for post in posts:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post.body)
        postbody = post.body
        for url in urls:
            postbody = postbody.replace(url, "<a href =\"" + url + "\">" + url + "</a>")
        print postbody
        postbodies.append(postbody)
    for i in range(0, len(posts)):
        user = models.User.query.filter_by(id=posts[i].user_id).first()
        usernames.append(user.name)

    if form.validate_on_submit():
        PostService.add_post(current_user.id, form.body.data, datetime.utcnow())
        return redirect('/posts')

    else:
        return render_template('t_posts.html', posts=posts, form=form, usernames=usernames, current_page=page,
                               postbodies=postbodies)


@app.route('/follow/<userid>', methods=['GET'])
@login_required
def follow(userid):
    print current_user.id
    fo = models.Follow(follow_id=current_user.id, followed_id=userid)
    db.session.add(fo)
    db.session.commit()
    return redirect('/userlist/all')


@app.route('/unfollow/<userid>', methods=['GET'])
@login_required
def unfollow(userid):
    fo = models.Follow.query.filter_by(follow_id=current_user.id, followed_id=userid).first()
    db.session.delete(fo)
    db.session.commit()
    return redirect('/userlist/following')


@app.route('/userlist/following')
@login_required
def following_user_list():
    users = []
    follows = models.Follow.query.filter_by(follow_id=current_user.id)
    for fo in follows:
        user = models.User.query.filter_by(id=fo.followed_id).first()
        users.append(user)
    return render_template('t_userlist.html', users=users)


@app.route('/userlist/all', methods=['GET'])
@login_required
def all_user_list():
    users = models.User.query.all()
    return render_template('t_userlist.html', users=users)


@app.route('/userlist', methods=['GET'])
def user_list():
    name = request.args.get('name')
    if len(name) == 0:
        return redirect('/userlist/all')
    else:
        user = UserService.get_user_by_name(name=name)
        users = []
        if user:
            users.append(user)
        return render_template('t_userlist.html', users=users)


@app.route('/userdetail/<user_id>')
@login_required
def user_detail(user_id):
    profile = models.UserProfile.query.filter_by(user_id=user_id).first()
    fo = models.Follow.query.filter_by(follow_id=current_user.id, followed_id=user_id).first()

    fo_exist = True
    if fo is None:
        fo_exist = False
    if profile:
        return render_template('t_userdetail.html', user_profile=profile, fo_exist=fo_exist)
    else:
        profile = models.UserProfile(user_info="Nothing here", avatar_url="", user_id=user_id)
        return render_template('t_userdetail.html', user_profile=profile, fo_exist=fo_exist)


@app.route('/me')
@login_required
def me():
    profile = models.UserProfile.query.filter_by(user_id=current_user.id).first()
    if profile:
        return render_template('t_userdetail.html', user_profile=profile)
    else:
        return redirect('/editprofile')


@app.route('/editprofile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = models.UserProfile.query.filter_by(user_id=current_user.id).first()
        if profile:
            profile.user_info = form.user_info.data
            profile.avatar_url = "temp_url"
            db.session.commit()
            return redirect('/me')
        else:
            new_profile = models.UserProfile(user_id=current_user.id, user_info=form.user_info.data,
                                             avatar_url="temp_url")
            db.session.add(new_profile)
            db.session.commit()
            return redirect('/me')
    return render_template('t_mypage_edit.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for username="%s", password=%s' %
              (form.name.data, form.password.data))
        user = models.User.query.filter_by(name=form.name.data).first()

        if user:
            if user.password == form.password.data:
                g.user = user
                print 'password correct'
                login_user(user)

                return redirect('/posts')
            else:
                print 'password wrong'
        else:
            return redirect('/error')
    else:
        return render_template('t_login.html', title='Login', form=form)


@app.route('/error')
def error():
    return 'error'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
