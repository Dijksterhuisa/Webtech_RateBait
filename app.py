from flask import Flask, render_template, flash, redirect, url_for
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from models import User, db
from forms import Registratie

app = Flask(__name__)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def index() -> str:
    """Homepage route."""
    return render_template("home.html")

@app.route("/rategames")
def bestemmingen() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    return render_template("rategames.html")

@app.route("/registratie", methods=["GET", "POST"])
def registratie() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    username: str | bool = False
    password: str | bool = False
    email:    str | bool = False

    form = Registratie()

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

if __name__ == "__main__":  
    app.run(debug=True)
    