from flask import render_template,redirect,url_for,abort
from ..models import User,Blog
from flask_login import login_required
from ..requests import get_quotes
from .forms import UpdateProfile,BlogForm
from .. import db,photos
from app.main import main
from wtforms import ValidationError


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to is Own your blog'

    
    blogs= Blog.get_all_blogs() 
    quotes = get_quotes() 

    return render_template('index.html', title = title, quotes = quotes, blogs= blogs)

@main.route('/all')
def all():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to is Own your blog'

    
    blogs= Blog.get_all_blogs() 
    

    return render_template('index.html', title = title, blogs= blogs)

@main.route('/blog/<int:blog_id>')
def blog(blog_id):

    '''
    View blog page function that returns the blog details page and its data
    '''
    found_blog= Blog.query.get(blog_id)
    title = blog_id
    # blog_comments = Comment.get_comments(blog_id)

    return render_template('blog.html',title= title ,found_blog= found_blog)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

