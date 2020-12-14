from flask import render_template,redirect,url_for,abort,request,flash
from ..models import User,Blog,Subscribe,ProfilePhoto,Comment
from flask_login import login_required,current_user
from ..requests import get_quotes
from .forms import UpdateProfile,BlogForm,CommentForm
from .. import db,photos
from app.main import main
from wtforms import ValidationError
import markdown2



@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


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


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to Own your blog'

    quotes = get_quotes() 
    return render_template('index.html', title = title, quotes = quotes)


@main.route('/blogs/all', methods= ['GET','POST'])
@login_required
def blogs_all():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Welcome to is Own your blog'    
    blogs= Blog.query.all() 
    quotes = get_quotes()
    
    return render_template('blogs.html', title = title, blogs= blogs, quotes=quotes)


@main.route('/blog/new', methods=['GET','POST'])
@login_required
def blog():
    """
    View blog function that returns the blog page and data
    """
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        description = blog_form.description.data
        new_blog = Blog(title=title, description=description, author=current_user)

        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.blog'))

    title = 'New Blog'
    return render_template('blog.html', title=title, blog_form=blog_form)


@main.route('/view/<int:id>', methods=['GET','POST'])
def view(id):

    '''
    View blog page function that returns the blog details page and its data
    '''
    blog = Blog.query.get_or_404(id)
    blog_comments = Comment.query.filter_by(blog_id=id).all()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
       new_comment = Comment(blog_id=id, comment=comment_form.comment.data, author=current_user)
       new_comment.save_comment()

    return render_template('view.html',blog=blog, blog_comments=blog_comments, comment_form=comment_form)


@main.route('/comment/<int:id>', methods=['GET','POST'])
@login_required
def comment(blog_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(blog_id=id, comment=comment.form.data, author=current_user.username)
        new_comment.save_comment()
        return redirect(url_for('main.blog'))

    return render_template('view.html', comment_form=comment_form)


@main.route('/Update/<int:id>', methods=['GET','POST'])
@login_required
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.author != current_user:
        abort(403)
    form = BlogForm()

    if form.validate_on_submit():
        blog.blog.title = form.blog.title.data
        blog.description = form.description.data
        db.session.commit()

        flash('Your post has been Updated', 'successfully')
        return redirect(url_for('main.blog'))

    elif request.method == 'GET':
        form.title.data = blog.title
        form.description.data = blog.description

    return render_template('update_blog.html', form=form)


@main.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    blog = Blog.query.get_or_404(id)
    if blog.author != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()

    flash('Your post has been deleted', 'successfully')
    return redirect(url_for('main.blog'))


@main.route('/subscribe', methods=['GET','POST'])
def subscribe():
    '''
    Function to send email upon subscription
    '''
    if request.method == 'POST':
        email = request.form['email']
        new_email = Subscribe(email=email)
        db.session.add(new_email)
        db.session.commit()
        flash('Thank you for your subscription')
        return redirect(url_for('main.index'))

