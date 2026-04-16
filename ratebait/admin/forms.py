from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class AdminReviewForm(FlaskForm):
    """Formulier voor het handmatig toevoegen of bewerken van reviews door een admin."""
    # We gebruiken een IntegerField voor de rating (1-5)
    rating = SelectField('Rating', choices=[
        (5, '⭐⭐⭐⭐⭐ Masterpiece'),
        (4, '⭐⭐⭐⭐ Great'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Mediocre'),
        (1, '⭐ Poor')
    ], coerce=int, default=3, validators=[DataRequired()])
    
    content = TextAreaField('Review Content', validators=[
        DataRequired(),
        Length(min=5, max=500, message="De review moet minstens 5 tekens lang zijn")
    ])
    
    # Optioneel: ID's handmatig koppelen (of je doet dit via de view)
    user_id = IntegerField('User ID', validators=[DataRequired()])
    game_id = IntegerField('Game ID', validators=[DataRequired()])
    
    submit = SubmitField('Save Review')

class AdminUserForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Admin Rechten') # Handig om anderen ook admin te maken
    submit = SubmitField('Gebruiker Opslaan')