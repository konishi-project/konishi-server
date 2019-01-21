"""
models.py
---
Database models, Security models, and Model Schemas.
"""
from app import app, ma, db, login
from flask import redirect, flash
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import UserMixin, login_required, current_user, logout_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_restplus import SchemaModel
from datetime import datetime

""" 
Defining the Models
---
Some of the items is directly from Flask-Security but modified to fit our needs.
Documentation - https://pythonhosted.org/Flask-Security/ 
"""
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    def __repr__(self):
        return '{} - {}'.format(self.name, self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ## User details
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(35), nullable=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Posts', backref='user')
    ## Likes 
    post_likes = db.relationship('PostLike', backref='user')
    comment_likes = db.relationship('CommentLike', backref='user')
    reply_like = db.relationship('ReplyLike', backref='user')
    ## Statuses
    joined_date = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '{}'.format(self.username)

"""
Used One to Many relationship for Posts.
Posts to Comments, Comments to Replies.
"""
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_name = db.Column(db.String(20))
    content = db.Column(db.Text)
    image_file = db.Column(db.String(35), nullable=True)
    status = db.Column(db.String(10))
    created = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    edited = db.Column(db.Boolean, default=False)
    likes = db.relationship('PostLike', backref='posts')
    comments = db.relationship('Comments', backref='posts')
    def __repr__(self):
        return 'Post ID - {}'.format(self.id)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    commenter = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    edited = db.Column(db.Boolean, default=False)
    likes = db.relationship('CommentLike', backref='comments')
    replies = db.relationship('Reply', backref='comments')
    def __repr__(self):
        return 'Comment ID - {}'.format(self.id)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Where this Reply belongs to which comment.
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replier = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    likes = db.relationship('ReplyLike', backref='reply')
    def __repr__(self):
        return 'Reply ID - {}'.format(self.id)

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    def __repr__(self):
        return '{}'.format(self.on_post)

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

class ReplyLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_reply = db.Column(db.Integer, db.ForeignKey('reply.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_on = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

## Model Schemas
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Posts

class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comments

class ReplySchema(ma.ModelSchema):
    class Meta:
        model = Reply

class PostLikeSchema(ma.ModelSchema):
    class Meta:
        model = PostLike

# Admin Index View is the Main Index, not the ModelView
class MainAdminIndexView(AdminIndexView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

# This is exactly similar to above Model but for ModelViews not Admin Index View.
class ProtectedModelView(ModelView):
    @login_required
    def is_accessible(self):
        # Check if the current user is an admin
        user = User.query.filter_by(username=current_user.username).first()
        if len(user.roles) > 0 and user.roles[0].name == 'admin':
            return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        logout_user()
        flash('Unathorized user!')
        return redirect('/adminlogin')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
