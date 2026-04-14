from models import db
from app import app

# Maak database bestand en tabellen aan
with app.app_context():
    db.create_all()