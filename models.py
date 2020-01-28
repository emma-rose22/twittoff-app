from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), nullable=False)

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280), nullable=False)