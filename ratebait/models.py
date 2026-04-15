from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, username: str, password: str, email: str):
        """Maakt een nieuw spel aan. Dit is waarschijnlijk nooit nodig.
        In:
            titel: titel van het spel
            cover_url: plaatje van het hoesje van het spel
        """
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        
    def __repr__(self):
        return f"<User {self.username}>"
    
    def check_password(self, password: str) -> bool:
        """Controleert het wachtwoord in de database tegenover het ingevoerde wachtwoord.
        
        In: Wachtwoord
        uit: Bool
        """
        return check_password_hash(self.password, password)
    
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
        return f"Deze review heeft {self.rating} sterren en is op {self.date_posted} gepost. Er is ook commentaar achtergelaten: {self.content}. User is {self.user_id}, Game is {self.game_id}"
    