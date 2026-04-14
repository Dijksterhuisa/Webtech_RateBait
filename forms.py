from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

class Registratie(FlaskForm):
    username = StringField("Gebruikersnaam")
    password = PasswordField("Wachtwoord")
    email =    StringField("Email, heel belangrijk, we sturen geen spam")
    submit = SubmitField('registreer')