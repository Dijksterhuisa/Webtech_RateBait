from flask import Blueprint, flash, render_template, request, redirect, url_for
from .forms import ReviewForm
from ratebait.models import db, Game, Review, User
from ratebait.api import search_game, get_game_by_id, format_cover_url
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# We maken een Blueprint aan in plaats van een Flask app
game_blueprint = Blueprint('game', __name__)

@game_blueprint.route('/rategames', methods=['GET', 'POST'])
def rategames():
    """Haalt de rategames pagina op. Bij een POST request wordt er gezocht naar games op basis van de zoekterm en worden deze weergegeven op de pagina.

    Returns:
        template: HTML template met zoekresultaten van games
    """
    games = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('search_query')
        if query:
            raw_results = search_game(query)
            if raw_results:
                seen_names = set()
                for item in raw_results:
                    name = item.get('name')
                    if name not in seen_names:
                        seen_names.add(name)
                        cover_data = item.get('cover')
                        cover_url = cover_data.get('url') if cover_data else None
                        games.append({
                            'id': item.get('id'),
                            'name': name,
                            'cover_url': format_cover_url(cover_url)
                        })
    
    return render_template('rategames.html', games=games, query=query)

@game_blueprint.route('/game/<int:game_id>')
def game_detail(game_id):
    """Haalt de detailpagina van een game op. Deze pagina toont de details van de game, een formulier om een review toe te voegen, en de bestaande reviews voor die game.

    Args:
        game_id (int): Het IGDB ID van de game wiens detailpagina opgehaald moet worden

    Returns:
        template: HTML template voor de detailpagina van een game
    """
    game_data = get_game_by_id(game_id)
    if not game_data:
        return "Game not found", 404

    cover_data = game_data.get('cover')
    cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
    
    db_game = db.session.get(Game, game_id)
    reviews = db_game.reviews if db_game else []
    form = ReviewForm()
    return render_template('game.html', game=game_data, form=form, cover_url=cover_url, reviews=reviews)

@game_blueprint.route('/game/<int:game_id>/review', methods=['POST'])
def add_review(game_id):
    """Laat een formulier zien om een review toe te voegen aan een game. Alleen toegankelijk voor ingelogde gebruikers.

    Args:
        game_id (int): Het IGDB ID van de game wiens review toegevoegd moet worden

    Returns:
        template: HTML template voor het toevoegen van een review
    """
    form = ReviewForm()
    
    if form.validate_on_submit():
        game = db.session.get(Game, game_id)
        if not game:
            api_game = get_game_by_id(game_id)
            cover_data = api_game.get('cover')
            cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
            game = Game(id=game_id, title=api_game.get('name'), cover_url=cover_url)
            db.session.add(game)
            db.session.commit()
        
        # We gebruiken current_user van Flask-Login om de ingelogde gebruiker te krijgen
        user = current_user if current_user.is_authenticated else None
        if not user:
            flash("Je moet ingelogd zijn om een review toe te voegen.", "warning")
            return redirect(url_for('login'))

        
        new_review = Review(
            rating=form.rating.data,
            content=form.content.data,
            user_id=current_user.id,
            game_id=game.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash("Je review is toegevoegd!", "success")
    else:
        for error in form.errors.values():
            flash(f"Fout in review: {error[0]}", "danger")
    
    return redirect(url_for('game.game_detail', game_id=game_id))