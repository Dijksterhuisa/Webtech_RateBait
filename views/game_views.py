from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Game, Review, User
from api import search_game, get_game_by_id, format_cover_url

# We maken een Blueprint aan in plaats van een Flask app
game_blueprint = Blueprint('game', __name__)

@game_blueprint.route('/rategames', methods=['GET', 'POST'])
def rategames():
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
                    if name and name not in seen_names:
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
    game_data = get_game_by_id(game_id)
    if not game_data:
        return "Game not found", 404

    cover_data = game_data.get('cover')
    cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
    
    db_game = db.session.get(Game, game_id)
    reviews = db_game.reviews if db_game else []

    return render_template('game.html', game=game_data, cover_url=cover_url, reviews=reviews)

@game_blueprint.route('/game/<int:game_id>/review', methods=['POST'])
def add_review(game_id):
    rating = request.form.get('rating')
    content = request.form.get('content')

    # Game ophalen of aanmaken
    game = db.session.get(Game, game_id)
    if not game:
        api_game = get_game_by_id(game_id)
        cover_data = api_game.get('cover')
        cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
        game = Game(id=game_id, title=api_game.get('name'), cover_url=cover_url)
        db.session.add(game)

    # 2. Create a dummy user if one doesn't exist
    user = User.query.first()
    if not user:
        # Voeg hier het password veld toe!
        user = User(username="PlayerOne", email="player@example.com", password="dummy_password")
        db.session.add(user)
        db.session.commit()

    review = Review(rating=int(rating), content=content, user_id=user.id, game_id=game.id)
    db.session.add(review)
    db.session.commit()

    # Let op: bij Blueprints gebruik je 'blueprintnaam.functienaam' in url_for
    return redirect(url_for('game.game_detail', game_id=game_id))