from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    '''Gebruikers voor de website'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.string(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Dit linkt de reviews aan een gebruiker als autheur.
    reviews = db.relationship('Review', backref='author', lazy=True)
  
    def __init__(self, username: str, password: str, email: str):
        """Maak nieuwe gebruiker aan.
        In:
            gebruikersnaam: gebruikersnaam
        """
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"gebruikersnaam is {self.username}, wachtwoord is (Haha, jij bent grappig. Hier print ik toch geen wachtwoord) en het email adres is {self.email}"
    
class Game(db.Model):
    '''De spellen voor onze review website. Deze worden opgehaald van  https://www.igdb.com/'''
    # We gebruiken de IGDB ID om geen duplicaten te hebben.
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(500))
    # Dit linkt het spel aan alle reviews ervan.
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
        return f"dit spel is {self.title} en de url naar het hoesje is {self.cover.url}."

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # 1-5 stars
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
 
    def __init__(self, rating: str, content: str, date_posted: str):
        """Maakt een nieuwe review aan.
        In:
            rating: Hoeveel sterren je het spel geeft 1/5
            content: commentaar bij de review
            date_posted: wanneer hij upgeload is.
        """
        self.title = title
        self.cover_url = cover_url

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"Deze review heeft {self.rating} sterren en is op {self.date_posted} gepost. Er is ook commentaar achtergelaten: {self.content}"