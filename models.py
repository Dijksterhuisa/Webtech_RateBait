class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Use the IGDB or Steam ID
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(500))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    rating = db.Column(db.Integer) # 1-5 stars
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)