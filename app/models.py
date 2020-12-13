from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class ProfilePhoto(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class Quote:
    '''
    Quote class to define quote Objects
    '''

    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    photos = db.relationship('ProfilePhoto', backref = 'user', lazy = "dynamic")
    blog = db.relationship('Blog',backref = 'author',lazy = True)
    comments = db.relationship('Comment', backref='author', lazy=True)


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    

    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):
    '''
    Blog class to define Blog Objects
    '''
    __tablename__ = 'blog'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255), index = True)
    description = db.Column(db.String(255),index = True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    blog = db.relationship('Comment', backref='blog', passive_deletes=True)

    def save_blog(self):
        '''
        Function that saves blogs
        '''
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all_blogs(cls, id):
        '''
        Function that queries the database and returns all the blogs
        '''
        blogs = Blog.query.filter_by(id=id).all()
        return Blogs


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls, blog_id):
        comments = Comment.query.filter_by(post_id=blog_id).all()
        return comments
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f'Comments: {self.comment}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Subscribe(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50))
    

