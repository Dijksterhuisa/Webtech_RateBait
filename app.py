from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from models import db, Game, Review, User
from flask_sqlalchemy import SQLAlchemy
from api import search_game, get_game_by_id, format_cover_url
from views.game_views import game_blueprint # Importeer je blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# Registreer de blueprint
app.register_blueprint(game_blueprint)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

class loginform(FlaskForm):
    login = StringField("Wat is je gebruikersnaam?")
    submit = SubmitField('Log in')

@app.route("/")
def index() -> str:
    """Homepage route."""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    login: str | bool = False
    form = loginform()

    if form.validate_on_submit():
        flash("Gebruikersnaam ingediend!")
        login = form.login.data
        form.login.data = ""
        #return redirect(url_for('index'))
    
    return render_template("login.html", form = form, login=login)

if __name__ == "__main__":
    # Dit zorgt ervoor dat de tabellen worden aangemaakt als ze nog niet bestaan
    with app.app_context():
        db.create_all()
        print("Database tabellen succesvol aangemaakt!")
        
    app.run(debug=True)