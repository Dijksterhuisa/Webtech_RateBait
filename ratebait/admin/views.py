from flask import Blueprint, app, render_template, redirect, url_for, flash, request
from ratebait.models import db, User, Review, Game
from ratebait.admin.forms import AdminReviewForm, AdminUserForm
from flask_login import current_user
from functools import wraps
from flask import abort
from werkzeug.security import generate_password_hash


# 1. Definieer de Blueprint
# De template_folder 'templates' zorgt dat Flask in ratebait/admin/templates zoekt
admin_blueprint = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates'
)
def admin_required(f):
    """Een decorator die controleert of de huidige gebruiker een admin is. Als dat niet het geval is, wordt er een 403 Forbidden fout weergegeven.

    Args:
        f (function): De functie die beveiligd moet worden

    Returns:
        function: De beveiligde functie
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Checkt of de gebruiker admin rechten heeft. Als dat niet het geval is, wordt er een 403 Forbidden fout weergegeven.

        Returns:
            function: De beveiligde functie
        """
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# 2. De Dashboard Route (manage.html)
@admin_blueprint.route('/admin')
@admin_required
def manage():
    """Haalt het beheerpaneel op. Alleen toegankelijk voor admins.

    Returns:
        template: HTML template voor het beheerpaneel
    """
    return render_template('manage.html')

# 3. Overzicht van alle reviews (list.html)
@admin_blueprint.route('/admin/reviews')
@admin_required
def list_reviews():
    """Haalt een overzicht van alle reviews op. Alleen toegankelijk voor admins.

    Returns:
        template: HTML template voor het overzicht van reviews
    """
    # We halen alle reviews op om in de tabel te tonen
    all_reviews = Review.query.all()
    return render_template('review_list.html', reviews=all_reviews)

# 4. Overzicht van alle gebruikers (list.html hergebruikt of apart)
@admin_blueprint.route('/admin/users')
@admin_required
def list_users():
    """Haalt een overzicht van alle gebruikers op. Alleen toegankelijk voor admins.

    Returns:
        template: HTML template voor het overzicht van gebruikers
    """
    all_users = User.query.all()
    # Je kunt list.html hergebruiken of een aparte users_list.html maken
    return render_template('user_list.html', users=all_users, mode='users')

# REVIEW BEWERKEN (Update)
@admin_blueprint.route('/admin/review/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_review(id):
    """Haalt het formulier voor het bewerken van een review op. Alleen toegankelijk voor admins.

    Args:
        id (int): Het ID van de review die bewerkt moet worden

    Returns:
        template: HTML template voor het bewerken van een review
    """
    review = db.session.get(Review, id)
    if not review:
        abort(404)
        
    # We vullen het formulier met de huidige data van de review
    form = AdminReviewForm(obj=review)
    
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.content = form.content.data
        review.user_id = form.user_id.data
        review.game_id = form.game_id.data
        
        db.session.commit()
        flash(f"Review voor {review.game.title} is bijgewerkt!", "success")
        return redirect(url_for('admin.list_reviews'))
        
    return render_template('edit_review.html', form=form, review=review)

# 5. Review verwijderen - Bevestigingspagina (delete.html)
@admin_blueprint.route('/admin/review/delete/<int:id>', methods=['GET'])
@admin_required
def delete_review(id):
    """Haalt de bevestigingspagina voor het verwijderen van een review op. Alleen toegankelijk voor admins.

    Args:
        id (int): Het ID van de review die verwijderd moet worden

    Returns:
        template: HTML template voor de bevestigingspagina
    """
    review = db.session.get(Review, id)
    if not review:
        flash("Review niet gevonden.")
        return redirect(url_for('admin.list_reviews'))
    return render_template('delete.html', review=review)

# 6. De eigenlijke verwijder-actie (POST request vanuit delete.html)
@admin_blueprint.route('/admin/review/confirm_delete/<int:id>', methods=['POST'])
@admin_required
def confirm_delete(id):
    """De eigenlijke verwijder-actie voor een review. Alleen toegankelijk voor admins.

    Args:
        id (int): Het ID van de review die verwijderd moet worden

    Returns:
        template: HTML template voor de reviewlijst na verwijdering.
    """
    review = db.session.get(Review, id)
    if review:
        game_title = review.game.title if review.game else "Onbekend Spel"
        db.session.delete(review)
        db.session.commit()
        flash(f"Review voor {game_title} is verwijderd.")
    else:
        flash("Review niet gevonden.", "danger")
    return redirect(url_for('admin.list_reviews'))

# 7. Handmatig toevoegen (add.html)
@admin_blueprint.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def add_review():
    """Haalt het formulier voor het toevoegen van een review op. Alleen toegankelijk voor admins.

    Returns:
        template: HTML template voor het toevoegen van een review
    """
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

# GEBRUIKER BEWERKEN (Update)
@admin_blueprint.route('/admin/user/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    """Haalt het formulier voor het bewerken van een gebruiker op. Alleen toegankelijk voor admins.

    Args:
        id (int): Het ID van de gebruiker die bewerkt moet worden

    Returns:
        template: HTML template voor het bewerken van een gebruiker
    """
    user = db.session.get(User, id)
    if not user:
        abort(404)
        
    form = AdminUserForm(obj=user) # 'obj=user' vult het formulier alvast in
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        #Als je de is_admin kolom hebt:
        user.is_admin_db = form.is_admin.data
        
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
            
        db.session.commit()
        flash(f"Gebruiker {user.username} bijgewerkt!")
        return redirect(url_for('admin.list_users'))
        
    return render_template('edit_user.html', form=form, user=user)

# GEBRUIKER VERWIJDEREN (Delete)
@admin_blueprint.route('/admin/user/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    """Function die een gebruiker verwijdert. Alleen toegankelijk voor admins.

    Args:
        id (int): Het ID van de gebruiker die verwijderd moet worden

    Returns:
        template: HTML template voor de gebruikerslijst na verwijdering
    """
    if id == current_user.id:
        flash("Je kunt jezelf niet verwijderen!")
        return redirect(url_for('admin.list_users'))
        
    user = db.session.get(User, id)
    if user:
        for review in user.reviews:
            db.session.delete(review)
        db.session.delete(user)
        db.session.commit()
        flash("Gebruiker verwijderd.")
    return redirect(url_for('admin.list_users'))

# HANDMATIG GEBRUIKER TOEVOEGEN
@admin_blueprint.route('/admin/user/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Haalt het formulier voor het toevoegen van een gebruiker op. Alleen toegankelijk voor admins.

    Returns:
        template: HTML template voor het toevoegen van een gebruiker
    """
    form = AdminUserForm()
    if form.validate_on_submit():
        # Let op: Je User model __init__ verwacht: username, password, email, is_admin
        # We geven hier een tijdelijk wachtwoord mee of je moet een password veld in AdminUserForm zetten
        new_user = User(
            username=form.username.data,
            password="StandaardWachtwoord123!", # Of haal uit form als je dat toevoegt
            email=form.email.data,
            is_admin=False # Of form.is_admin.data als je die hebt
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"Gebruiker {new_user.username} is toegevoegd!")
        return redirect(url_for('admin.list_users'))
    
    return render_template('edit_user.html', form=form, user=None)