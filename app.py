from flask import Flask, render_template, flash, request, redirect, url_for, Blueprint
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from ratebait.models import db, Game, Review, User
from flask_sqlalchemy import SQLAlchemy
from ratebait.game.views import game_blueprint
from ratebait.users.views import user_blueprint
from ratebait.users.forms import RegistratieForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, template_folder='ratebait/templates')

# Registreer de blueprint
app.register_blueprint(game_blueprint)
app.register_blueprint(user_blueprint)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

@app.route("/")
def index() -> str:
    """Homepage route."""
    return render_template("home.html")

@app.route("/registratie", methods=["GET", "POST"])
def registratie() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    username: str | bool = False
    password: str | bool = False
    email:    str | bool = False

    form = RegistratieForm()

    if form.validate_on_submit():
        flash("Account aangemaakt!")

        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User(username,password,email)
        db.session.add(user)
        db.session.commit()

        form.username.data = ""
        form.password.data = ""
        form.email.data = "" 
    
    return render_template("registratie.html", form = form, username=username, password=password, email=email)

@app.route("/users", methods=["GET", "POST"])
def users() -> str:
    users = db.session.execute(db.select(User.username)).scalars().all()
    
    return render_template('users.html', users=users)    

@app.route("/reviews", methods=["GET", "POST"])
def reviews() -> str:
    reviews = db.session.execute(db.select(Review)).scalars().all()
    return render_template('reviews.html', reviews=reviews)


@app.route("/login", methods=["GET", "POST"])
def registratie() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    username: str | bool = False
    password: str | bool = False
    email:    str | bool = False

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and User.check_password(form.password.data):
            login_user(user)
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for("index"))
        else:
            flash("Ongeldige gebruikersnaam of wachtwoord", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Je bent uitgelogd!", "info")
    return redirect(url_for("index"))

@app.route("/geheim")
@login_required
def geheim():
    return "Alleen zichtbaar voor ingelogde gebruikers!"



if __name__ == "__main__": 
    # Dit zorgt ervoor dat de tabellen worden aangemaakt als ze nog niet bestaan
    with app.app_context():
        db.create_all()
        print("Database tabellen succesvol aangemaakt!")
    app.run(debug=True)
    