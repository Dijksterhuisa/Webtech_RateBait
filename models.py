from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # This links the user to their reviews
    reviews = db.relationship('Review', backref='author', lazy=True)

class Game(db.Model):
    # We use the IGDB ID as our primary key so we don't duplicate games
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(500))
    # This links the game to all reviews written about it
    reviews = db.relationship('Review', backref='game', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # 1-5 stars
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)