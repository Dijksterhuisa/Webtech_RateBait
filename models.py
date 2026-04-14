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
   
    def __init__(self, title: str, cover_url: str):
        """Maakt een nieuw spel aan. Dit is waarschijnlijk nooit nodig.
        In:
            titel: titel van het spel
            cover_url: plaatje van het hoesje van het spel
        """
        self.title = title
        self.cover_url = cover_url

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"dit spel is {self.title} en de url naar het hoesje is {self.cover_url}."

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
 
    def __init__(self, rating: str, content: str, date_posted: str):
        """Maakt een nieuwe review aan.
        In:
            rating: Hoeveel sterren je het spel geeft 1/5
            content: commentaar bij de review
            date_posted: wanneer hij upgeload is.
        """
        self.rating = rating
        self.content = content
        self.date_posted = date_posted

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"Deze review heeft {self.rating} sterren en is op {self.date_posted} gepost. Er is ook commentaar achtergelaten: {self.content}"