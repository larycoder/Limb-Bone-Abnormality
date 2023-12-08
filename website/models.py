from . import db
from flask_login import UserMixin
from sqlalchemy.sql  import func

class User(db.Model, UserMixin):
    role = db.Column(db.Integer, default = 2)
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable= False)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    files = db.relationship('File')


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime(timezone = True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class File(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    path = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime(timezone= True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))