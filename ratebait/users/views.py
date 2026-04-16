from flask import Blueprint, flash, redirect, render_template, abort, url_for
from flask_login import current_user, login_required
from ratebait.admin.views import admin_required
from ratebait.models import Review, User, db
from flask import Blueprint, render_template
from .forms import EditReviewForm

user_blueprint = Blueprint(
    'users', 
    __name__, 
    template_folder='templates'
)

@user_blueprint.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    # Haal de gebruiker op, of geef een 404 als hij niet bestaat
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    
    # Omdat we 'backref=author' hebben in models.py, 
    # kunnen we simpelweg user.reviews gebruiken.
    return render_template('profile.html', user=user, reviews=user.reviews)

@user_blueprint.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_my_review(review_id):
    review = db.session.get(Review, review_id)
    
    if not review:
        abort(404)
        
    if not current_user.is_admin and review.author.id != current_user.id:
        abort(403) # Verboden als het niet jouw review is
        
    form = EditReviewForm(obj=review) # Vul formulier met huidige data
    
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.content = form.content.data
        db.session.commit()
        flash("Je review is succesvol bijgewerkt!", "success")
        return redirect(url_for('users.profile', user_id=current_user.id))
        
    return render_template('edit_review.html', form=form, review=review)

@user_blueprint.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_my_review(review_id):
    review = db.session.get(Review, review_id)
    
    if not review:
        abort(404)

    # Check: Ben jij de eigenaar OF ben je admin?
    if review.author.id != current_user.id and not current_user.is_admin:
        abort(403)

    db.session.delete(review)
    db.session.commit()
    flash("Je review is definitief verwijderd.", "success")
    
    return redirect(url_for('users.profile', user_id=current_user.id))