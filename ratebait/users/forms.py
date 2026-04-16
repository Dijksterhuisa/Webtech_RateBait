from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistratieForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Wachtwoord", validators=[DataRequired(), Length(min=6, max=100)])
    email =    StringField("Email, heel belangrijk, we sturen geen spam", validators=[DataRequired(), Length(max=100), Email()])
    submit = SubmitField('registreer')

class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("inloggen")
    
class EditReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '⭐⭐⭐⭐⭐ Masterpiece'),
        (4, '⭐⭐⭐⭐ Great'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Mediocre'),
        (1, '⭐ Poor')
    ], coerce=int, default=3, validators=[DataRequired()])
    
    content = TextAreaField('Jouw Review', validators=[
        DataRequired(), 
        Length(min=10, max=500, message="Je review moet tussen de 10 en 500 tekens zijn.")
    ])
    
    submit = SubmitField('Wijzigingen Opslaan')
    