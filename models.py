from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Game(db.Model):
    # Belangrijk: Geen autoincrement omdat we IGDB ID's gebruiken
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) 
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(500))
    reviews = db.relationship('Review', backref='game', lazy=True)

    def __repr__(self):
        return f"<Game {self.title}>"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return f"<Review {self.rating}* - {self.content[:20]}...>"