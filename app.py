import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from models import db, Game, Review, User
from api import search_game, get_game_by_id, format_cover_url

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamevault.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    games = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('search_query')
        if query:
            raw_results = search_game(query)
            if raw_results:
                for item in raw_results:
                    cover_data = item.get('cover')
                    cover_url = cover_data.get('url') if cover_data else None
                    games.append({
                        'id': item.get('id'), # Capture the ID so we can link to it
                        'name': item.get('name'),
                        'cover_url': format_cover_url(cover_url)
                    })
    
    return render_template('index.html', games=games, query=query)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    # 1. Fetch game details from the API
    game_data = get_game_by_id(game_id)
    if not game_data:
        return "Game not found", 404

    cover_data = game_data.get('cover')
    cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
    
    # 2. Fetch local reviews from our database
    db_game = Game.query.get(game_id)
    reviews = db_game.reviews if db_game else []

    return render_template('game.html', game=game_data, cover_url=cover_url, reviews=reviews)

@app.route('/game/<int:game_id>/review', methods=['POST'])
def add_review(game_id):
    rating = request.form.get('rating')
    content = request.form.get('content')

    # 1. Check if the game is in our database yet. If not, add it.
    game = Game.query.get(game_id)
    if not game:
        api_game = get_game_by_id(game_id)
        cover_data = api_game.get('cover')
        cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
        
        game = Game(id=game_id, title=api_game.get('name'), cover_url=cover_url)
        db.session.add(game)

    # 2. Create a dummy user if one doesn't exist (since we don't have a login system yet)
    user = User.query.first()
    if not user:
        user = User(username="PlayerOne", email="player@example.com")
        db.session.add(user)
        db.session.commit() # Commit the user so they get an ID

    # 3. Save the review
    review = Review(rating=int(rating), content=content, user_id=user.id, game_id=game.id)
    db.session.add(review)
    db.session.commit()

    return redirect(url_for('game_detail', game_id=game_id))

if __name__ == '__main__':
    app.run(debug=True)