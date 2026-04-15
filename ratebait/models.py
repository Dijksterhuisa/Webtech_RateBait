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
        return check_password_hash(self.password_hash, password)