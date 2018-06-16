#from main import app
from flask_wtf import FlaskForm
from wtforms.validators import Required
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy(app)
db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #users = db.relationship('User', backref='role', lazy='dynamic')
    
    #users_primary_role = db.relationship('User', primaryjoin='Role.id==User.primary_role_id')
    #users_secondary_role = db.relationship('User', primaryjoin='Role.id==User.secondary_role_id')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #email = db.Column(db.String(120), unique=True, nullable=False, server_default='')
    #intro = db.Column(db.String(200))
    #primary_role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #secondary_role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #primary_role = db.relationship('Role', foreign_keys='User.primary_role_id')
    #secondary_role = db.relationship('Role', foreign_keys='User.secondary_role_id')

    #def __init__(self, username, email):
    #    self.username = username
    #    self.email = email

    def __repr__(self):
        return "<User: %r>" % self.username

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
