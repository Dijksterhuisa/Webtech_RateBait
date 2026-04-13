from flask import Flask, render_template, flash, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

app = Flask(__name__)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

class loginform(FlaskForm):
    login = StringField("Wat is je gebruikersnaam?")
    submit = SubmitField('Log in')

@app.route("/")
def index() -> str:
    """Homepage route."""
    return render_template("home.html")

@app.route("/rategames")
def bestemmingen() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    return render_template("rategames.html")

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
    app.run(debug=True)