from . import db
from flask_login import UserMixin
from sqlalchemy.sql  import func

class User(db.Model, UserMixin):
    role = db.Column(db.Integer, default = 2)
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable= False)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    folder_user = db.Column(db.String(50))

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    path = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

class File(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    path = db.Column(db.String(50), nullable = False)
    data = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime(timezone= True), default=func.now())
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    folder=db.relationship('Folder')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")