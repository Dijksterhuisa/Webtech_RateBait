from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '⭐⭐⭐⭐⭐ Masterpiece'),
        (4, '⭐⭐⭐⭐ Great'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Mediocre'),
        (1, '⭐ Poor')
    ], coerce=int, default=3, validators=[DataRequired()])
    content = TextAreaField('Review', validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField('Post Review')