from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# GET all games
@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()]
    return make_response(games, 200)

# GET one game by ID (with reviews)
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if not game:
        return make_response({"error": "Game not found"}, 404)
    return make_response(game.to_dict(), 200)

# GET users who reviewed a specific game
@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if not game:
        return make_response({"error": "Game not found"}, 404)
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    return make_response(users, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
