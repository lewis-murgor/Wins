from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    wins = db.relationship('Win',backref = 'user',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic")
    upvotes = db.relationship('UpVote',backref = 'user',lazy="dynamic")

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

class Win(db.Model):
    __tablename__ = 'wins'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.String)
    photo_path = db.Column(db.String(),nullable = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref = 'blog',lazy="dynamic")
    upvotes = db.relationship('UpVote',backref = 'pitch',lazy="dynamic")

    def save_win(self):
        
        db.session.add(self)
        db.session.commit()

    def delete_win(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_wins(cls):

        return Win.query.all()

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(700))
    win_id = db.Column(db.Integer,db.ForeignKey('wins.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments

    def __repr__(self):
        return f'User {self.comment}'

class UpVote(db.Model):
    __tablename__= 'upvotes'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    win_id = db.Column(db.Integer,db.ForeignKey('wins.id'))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,id):
        upvotes = UpVote.query.filter_by(id = id).all()
        return upvotes

    @classmethod
    def get_user_vote(cls, user_id):
        user_vote = UpVote.query.filter_by(id = user_id).all()
        return user_vote

    def __repr__(self):
        return f'User {self.id}'

