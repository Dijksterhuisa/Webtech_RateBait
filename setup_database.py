from basic_model_app import app, db, Gebruiker

# Maak database bestand en tabellen aan
with app.app_context():
    db.create_all()