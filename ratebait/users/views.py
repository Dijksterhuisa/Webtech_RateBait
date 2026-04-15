from flask import Blueprint, render_template, abort
from ratebait.models import User, db
from flask import Blueprint, render_template

user_blueprint = Blueprint(
    'users', 
    __name__, 
    template_folder='templates'
)

@user_blueprint.route('/profile/<int:user_id>')
def profile(user_id):
    # Haal de gebruiker op, of geef een 404 als hij niet bestaat
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    
    # Omdat we 'backref=author' hebben in models.py, 
    # kunnen we simpelweg user.reviews gebruiken.
    return render_template('users.html', user=user, reviews=user.reviews)