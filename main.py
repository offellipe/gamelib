from flask import Flask, render_template, request,  redirect, session, flash, url_for
from models.Game import Game
from models.User import User

game1 = Game('Elden Ring', 'Souls Like', 'Cross')
game2 = Game('God of War', 'Adventure', 'Playstation')
game3 = Game('Dark Souls', 'Souls Like', 'Cross')

game_list = [game1, game2, game3]

user1 = User('Fellipe', 'offellipe', 'Biachocolate1504@')
user2 = User('Natan', 'natan001', 'alohomora10')
user3 = User('Alan', 'alan002', '12345@')

user_list = {user1.username: user1,
             user2.username: user2,
             user3.username: user3}

app = Flask(__name__)
app.secret_key = 'offellipe'

@app.route('/')
def index():
    return render_template('list.html', title='Games available', games=game_list)

@app.route('/newgame')
def new_game():
    if 'user_active' not in session or session['user_active'] == None:
        return redirect(url_for('login', next=url_for('new_game')))
    else:
        return render_template('newgame.html', title='New Game')

@app.route('/create', methods=['POST'],)
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name, category, console)
    game_list.append(game)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/authenticate', methods=['POST',])
def authenticate():
    if request.form['user'] in user_list:
        user = user_list[request.form['user']]
        if request.form['passoword'] == user.password:
            session['user_active'] = user.username
            flash(user.username + ' logged in successfully ')
            next_page = request.form['next']
            return redirect(next_page)
        else:
            flash('Login error: maybe the access data is wrong')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user_active'] == None
    flash('Logout done successfully')
    return redirect(url_for('index'))


app.run(debug=True)
