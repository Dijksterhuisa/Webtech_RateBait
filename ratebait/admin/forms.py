from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class AdminReviewForm(FlaskForm):
    """Formulier voor het handmatig toevoegen of bewerken van reviews door een admin."""
    # We gebruiken een IntegerField voor de rating (1-5)
    rating = IntegerField('Rating (1-5)', validators=[
        DataRequired(), 
        NumberRange(min=1, max=5, message="Kies een score tussen 1 en 5")
    ])
    
    content = TextAreaField('Review Content', validators=[
        DataRequired(),
        Length(min=5, message="De review moet minstens 5 tekens lang zijn")
    ])
    
    # Optioneel: ID's handmatig koppelen (of je doet dit via de view)
    user_id = IntegerField('User ID', validators=[DataRequired()])
    game_id = IntegerField('Game ID', validators=[DataRequired()])
    
    submit = SubmitField('Save Review')

class AdminUserForm(FlaskForm):
    """Formulier voor het beheren van gebruikers (bijv. wachtwoord reset of email aanpassing)."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password (leave blank to keep current)')
    
    submit = SubmitField('Update User')