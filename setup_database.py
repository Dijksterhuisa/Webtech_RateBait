from basic_model_app import app, db, Gebruiker

# Maak database bestand en tabellen aan
with app.app_context():
    db.create_all()

    # Maak objecten aan
    joyce = Gebruiker('Joyce')
    bram = Gebruiker('Bram')

    # Voeg toe aan database sessie
    db.session.add_all([joyce, bram])

    # Schrijf definitief naar database
    db.session.commit()

    print(joyce.id)  # 1
    print(bram.id)   # 2