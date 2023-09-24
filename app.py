import os
from datetime import datetime
# import pandas as pd
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
players = []

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///score.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template('login.html')

@app.route("/landlord_player", methods=["GET", "POST"])
def landlord_player():
    if request.method == 'GET':

        return render_template('landlord_player.html')

    else:
        # print('AAA')
        player1 = request.form.get('player1')
        player2 = request.form.get('player2')
        player3 = request.form.get('player3')
        # print(player1)
        session['player1'] = player1.upper().strip()
        session['player2'] = player2.upper().strip()
        session['player3'] = player3.upper().strip()

        db_dict = db.execute('SELECT * FROM score')
        # print('AAAAA')
        key_lst = list(db_dict[0].keys())
        name_lst = [name.upper() for name in key_lst]


        if session['player1'].strip().upper() not in name_lst:

            db.execute('ALTER TABLE score ADD ? int', session['player1'])

        if session['player2'].strip().upper() not in name_lst:
            db.execute('ALTER TABLE score ADD ? int',session['player2'])

        if session['player3'].strip().upper() not in name_lst:
            db.execute('ALTER TABLE score ADD ? int',session['player3'])

        return redirect('/landlord')
        # return render_template('landlord.html')

@app.route('/landlord', methods = ['GET', 'POST'])
def landlord():
    today = datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        id = request.form.get("id")

        if id:

            db.execute("DELETE FROM score WHERE id = ?", id)
            return redirect('/landlord')

        landlord = request.form.get('landlord')
        outcome = request.form.get('outcome')
        num_bomb = int(request.form.get('num_bomb'))



        if outcome == 'Win':
            print(landlord)
            landlord_score = 2 * (2**num_bomb)
            people_score = - (2**num_bomb)

            if session['player1'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, landlord_score, people_score, people_score)
            elif session['player2'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, people_score, landlord_score, people_score)
            elif session['player3'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, people_score, people_score, landlord_score)

        elif outcome == 'Lose':
            landlord_score =  -2 * (2**num_bomb)
            people_score = 2**num_bomb
            print(landlord_score)
            print(people_score)

            if session['player1'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, landlord_score, people_score, people_score)
            elif session['player2'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, people_score, landlord_score, people_score)
            elif session['player3'] == landlord:
                db.execute('INSERT INTO score (date,?,?,?) VALUES (?,?,?,?)', session['player1'], session['player2'], session['player3'], today, people_score, people_score, landlord_score)

        return redirect('/landlord')


    elif request.method == 'GET':
        player1 = session['player1'].upper().strip()
        player2 = session['player2'].upper().strip()
        player3 = session['player3'].upper().strip()

        query = f'SELECT id, {player1}, {player2}, {player3} FROM score WHERE date = "{today}"'
        # print('AAAA')
        # print(query)
        scores = db.execute(query)
        # print(scores)

        total_score = db.execute(f'SELECT sum({player1}) AS tot1, sum({player2}) AS tot2, sum({player3}) AS tot3 FROM score WHERE date = "{today}"')
        print(total_score)

        return render_template('landlord.html', player1 = session['player1'], player2 = session['player2'], player3 = session['player3'],
        date = today, scores = scores, total_score = total_score)

# app.run()


@app.route("/mah_jong_player", methods=["GET", "POST"])
def mah_jong_player():
    if request.method == 'GET':
        print('AAAA')
        return render_template('mah_jong_player.html')

    else:
        # print('AAA')
        player1 = request.form.get('player1')
        player2 = request.form.get('player2')
        player3 = request.form.get('player3')
        player4 = request.form.get('player4')
        # print(player1)
        session['player1'] = player1.upper().strip()
        session['player2'] = player2.upper().strip()
        session['player3'] = player3.upper().strip()
        session['player4'] = player4.upper().strip()

        db_dict = db.execute('SELECT * FROM score_mh')
        # print('AAAAA')
        key_lst = list(db_dict[0].keys())
        name_lst = [name.upper() for name in key_lst]
        if session['player1'] not in name_lst:
            db.execute('ALTER TABLE score_mh ADD ? int', session['player1'])

        if session['player2'] not in name_lst:
            db.execute('ALTER TABLE score_mh ADD ? int',session['player2'])

        if session['player3'] not in name_lst:
            db.execute('ALTER TABLE score_mh ADD ? int',session['player3'])

        if session['player4'] not in name_lst:
            db.execute('ALTER TABLE score_mh ADD ? int',session['player4'])

        return redirect('/mah_jong')

@app.route('/mah_jong', methods = ['GET', 'POST'])
def mah_jong():
    today = datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':

        id = request.form.get("id")
        print('AAAAAAA')
        print(id)
        if id:
            print('AAAAAAAAAAAA')
            db.execute("DELETE FROM score_mh WHERE id = ?", id)
            return redirect('/mah_jong')


        winner = request.form.get('winner')
        method = request.form.get('method')
        loser = request.form.get('loser')
        num_fan = int(request.form.get('num_fan'))




        if method == 'self':
            # print(landlord)
            winner_score = int(1.5 * 2**num_fan)
            people_score = - int(winner_score/3)

            if session['player1'] == winner:
                db.execute('INSERT INTO score_mh (date,?,?,?,?) VALUES (?,?,?,?,?)',
                session['player1'], session['player2'], session['player3'], session['player4'], today, winner_score, people_score, people_score, people_score)

            elif session['player2'] == winner:
                db.execute('INSERT INTO score_mh (date,?,?,?, ?) VALUES (?,?,?,?, ?)',
                session['player1'], session['player2'], session['player3'], session['player4'], today, people_score, winner_score, people_score, people_score)

            elif session['player3'] == winner:
                db.execute('INSERT INTO score_mh (date,?,?,?, ?) VALUES (?,?,?,?, ?)',
                session['player1'], session['player2'], session['player3'], session['player4'], today, people_score, people_score, winner_score, people_score)

            elif session['player4'] == winner:
                db.execute('INSERT INTO score_mh (date,?,?,?, ?) VALUES (?,?,?,?, ?)',
                session['player1'], session['player2'], session['player3'], session['player4'], today, people_score, people_score, people_score, winner_score)

        elif method == 'other':
            winner_score = 2**num_fan
            loser_score = -winner_score/2
            people_score = -winner_score/4



            people_lst = [session['player1'], session['player2'], session['player3'], session['player4']]

            people_lst.remove(winner)
            people_lst.remove(loser)

            db.execute('INSERT INTO score_mh (date,?,?,?,?) VALUES (?,?,?,?,?)',
            winner, loser, people_lst[0], people_lst[1], today, winner_score, loser_score, people_score, people_score)

        return redirect('/mah_jong')


    elif request.method == 'GET':
        player1 = session['player1']
        player2 = session['player2']
        player3 = session['player3']
        player4 = session['player4']
        id = request.form.get("id")


        query = f'SELECT id, {player1}, {player2}, {player3}, {player4} FROM score_mh WHERE date = "{today}"'
        # print('AAAA')
        # print(query)
        scores = db.execute(query)
        print(scores)
        # print(scores)

        total_score = db.execute(f'SELECT sum({player1}) AS tot1, sum({player2}) AS tot2, sum({player3}) AS tot3, sum({player4}) AS tot4 FROM score_mh WHERE date = "{today}"')
        # print(total_score)

        return render_template('mah_jong.html', player1 = session['player1'], player2 = session['player2'], player3 = session['player3'],
        player4 = session['player4'], date = today, scores = scores, total_score = total_score)
