 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///squid_game.db'
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Game %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    progress = db.relationship('Progress', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Progress %r>' % self.score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<int:game_id>')
def game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game.html', game=game)

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/progress')
def progress():
    user = current_user
    progress = Progress.query.filter_by(user_id=user.id).all()
    return render_template('progress.html', progress=progress)

if __name__ == '__main__':
    app.run()
