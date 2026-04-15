from flask import Blueprint, render_template, redirect, url_for, flash, request
from ratebait.models import db, User, Review, Game
from ratebait.admin.forms import AdminReviewForm

# 1. Definieer de Blueprint
# De template_folder 'templates' zorgt dat Flask in ratebait/admin/templates zoekt
admin_blueprint = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates'
)

# 2. De Dashboard Route (manage.html)
@admin_blueprint.route('/admin')
def manage():
    return render_template('manage.html')

# 3. Overzicht van alle reviews (list.html)
@admin_blueprint.route('/admin/reviews')
def list_reviews():
    # We halen alle reviews op om in de tabel te tonen
    all_reviews = Review.query.all()
    return render_template('review_list.html', reviews=all_reviews)

# 4. Overzicht van alle gebruikers (list.html hergebruikt of apart)
@admin_blueprint.route('/admin/users')
def list_users():
    all_users = User.query.all()
    # Je kunt list.html hergebruiken of een aparte users_list.html maken
    return render_template('user_list.html', users=all_users, mode='users')

# 5. Review verwijderen - Bevestigingspagina (delete.html)
@admin_blueprint.route('/admin/review/delete/<int:id>', methods=['GET'])
def delete_review(id):
    review = db.session.get(Review, id)
    if not review:
        flash("Review niet gevonden.")
        return redirect(url_for('admin.list_reviews'))
    return render_template('delete.html', review=review)

# 6. De eigenlijke verwijder-actie (POST request vanuit delete.html)
@admin_blueprint.route('/admin/review/confirm_delete/<int:id>', methods=['POST'])
def confirm_delete(id):
    review = db.session.get(Review, id)
    if review:
        db.session.delete(review)
        db.session.commit()
        flash(f"Review voor {review.game.title} is verwijderd.")
    return redirect(url_for('admin.list_reviews'))

# 7. Handmatig toevoegen (add.html)
@admin_blueprint.route('/admin/add', methods=['GET', 'POST'])
def add_review():
    form = AdminReviewForm()
    
    if form.validate_on_submit():
        # Hier verwerk je de data als op 'Submit' wordt geklikt
        new_review = Review(
            rating=form.rating.data,
            content=form.content.data,
            user_id=form.user_id.data,
            game_id=form.game_id.data
        )
        db.session.add(new_review)
        db.session.commit()
        flash("Review succesvol toegevoegd!")
        return redirect(url_for('admin.list_reviews'))
    
    # Nu stuur je 'form' eindelijk mee naar de template!
    return render_template('add.html', form=form)