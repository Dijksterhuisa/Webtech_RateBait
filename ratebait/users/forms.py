from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, 
from wtforms.validators import DataRequired

class RegistratieForm(FlaskForm):
    username = StringField("Gebruikersnaam")
    password = PasswordField("Wachtwoord")
    email =    StringField("Email, heel belangrijk, we sturen geen spam")
    submit = SubmitField('registreer')

class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("inloggen")