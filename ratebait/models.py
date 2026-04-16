from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

### Database definitie ###
db = SQLAlchemy()


### Tabel users ###
class User(db.Model,UserMixin):
    """Database tabel met de onderstaande rijen. Heeft een relatie met reviews. Een review heeft een autheur en een user kan reviews hebben."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='author', lazy=True)
    is_admin_db = db.Column(db.Boolean, default=False)

    @property
    def is_admin(self):
        """Geeft aan of de gebruiker admin rechten heeft."""
        return self.is_admin_db
    
    def __init__(self, username: str, password: str, email: str, is_admin: bool):
        """Maakt een nieuwe gebruiker aan.
        IN: username, password en email in str format en is_admin in bool format
        OUT: Een database entrie.
        """
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.is_admin_db = is_admin

    def __repr__(self):
        """ Print informatie over de class"""
        return f"User is {self.username} en email is {self.email}. Het wachtwoord is (Haha, ik deel geen wachtwoord met jou)"
    
    def check_password(self, password: str) -> bool:
        """Controleert het wachtwoord in de database tegenover het ingevoerde wachtwoord.
        
        In: Wachtwoord
        uit: Bool
        """
        return check_password_hash(self.password, password)
    
class Game(db.Model):
    """ Database tabel voor de spellen. Met de rijen ID, title, cover_url. Heeft een relatie met reviews. Een spel heeft reviews en een review heeft een spel."""
    # Belangrijk: Geen autoincrement omdat we IGDB ID's gebruiken
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) 
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(500))
    reviews = db.relationship('Review', backref='game', lazy=True)
    
    def __repr__(self):
        """Print een string over de class"""
        return f"<Game {self.title}>"

class Review(db.Model):
    """Database tabel voor de reviews, Met de rijen: id, rating, content, date_posted. Heeft een relatie met Users en games."""
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        """Een string met een uitleg over de class"""
        return f"Deze review heeft {self.rating} sterren en is op {self.date_posted} gepost. Er is ook commentaar achtergelaten: {self.content}. User is {self.user_id}, Game is {self.game_id}"
    