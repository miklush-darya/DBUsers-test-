
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask, redirect, request, render_template, url_for, make_response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test13.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('sqlite:///test13.db')



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500), nullable=True)

    j_n= db.relationship('Profiles', backref = 'users', uselist=False)

    def __repr__(self):
        return f'<users {self.id} {self.email} {self.password}>'

    def getUser(self, id):
        get_us = Users.query.filter_by(id = id).all()
        return get_us

    def getUserByEmail(self, email):
        get_us_email = Users.query.filter_by(email = email).all()
        return get_us_email



class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id} {self.name} {self.old} {self.city}>'
