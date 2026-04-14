from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from models import db, Game, Review, User
from flask_sqlalchemy import SQLAlchemy
from api import search_game, get_game_by_id, format_cover_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

class loginform(FlaskForm):
    login = StringField("Wat is je gebruikersnaam?")
    submit = SubmitField('Log in')

@app.route("/")
def index() -> str:
    """Homepage route."""
    return render_template("home.html")

@app.route('/rategames', methods=['GET', 'POST'])
def rategames():
    games = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('search_query')
        if query:
            raw_results = search_game(query)
            if raw_results:
                seen_names = set()  # Set om unieke gametitels bij te houden
                for item in raw_results:
                    name = item.get('name')
                    if name and name not in seen_names:
                        seen_names.add(name)
                        cover_data = item.get('cover')
                        cover_url = cover_data.get('url') if cover_data else None
                        games.append({
                            'id': item.get('id'), # Capture the ID so we can link to it
                            'name': item.get('name'),
                            'cover_url': format_cover_url(cover_url)
                        })
    
    return render_template('rategames.html', games=games, query=query)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    # 1. Fetch game details from the API
    game_data = get_game_by_id(game_id)
    if not game_data:
        return "Game not found", 404

    cover_data = game_data.get('cover')
    cover_url = format_cover_url(cover_data.get('url') if cover_data else None)
    
    # 2. Fetch local reviews from our database
    db_game = db.session.get(Game, game_id)
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


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """W.I.P bestemmingen pagina voor testen van navbar W.I.P"""
    login: str | bool = False
    form = loginform()

    if form.validate_on_submit():
        flash("Gebruikersnaam ingediend!")
        login = form.login.data
        form.login.data = ""
        #return redirect(url_for('index'))
    
    return render_template("login.html", form = form, login=login)




if __name__ == "__main__":
    # Dit zorgt ervoor dat de tabellen worden aangemaakt als ze nog niet bestaan
    with app.app_context():
        db.create_all()
        print("Database tabellen succesvol aangemaakt!")
        
    app.run(debug=True)