import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Gebruiker(db.Model):
    """Model voor gebruikers van ratebait"""

    __tablename__ = 'gebruikers'
    id: Mapped[int] = mapped_column(primary_key=True)
    gebruikersnaam: Mapped[str | None]

    def __init__(self, gebruikersnaam: str):
        """Maak nieuwe gebruiker aan.
        In:
            gebruikersnaam: gebruikersnaam
        """
        self.gebruikersnaam = gebruikersnaam

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"gebruikersnaam is {self.gebruikersnaam}"
    
