# ..................................Set Up

import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request, flash
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
from operator import itemgetter
from functions import write_to_file, check_in_file, clear_text_file, print_content_in_list, check_answer, store_incorrect_answers, right_or_wrong, question_selector, increase_user_score, add_to_leaderboard, order_leaderboard, setup_leaderboard, next_player, leaderboard_len, next_round, reset_turn, q_update, get_winner, question_update

app = Flask(__name__)

# ..................................Template Page Functions

@app.route('/', methods=["GET", "POST"])
def index():
    # User(s) enter the number of players in the game #
    setup_leaderboard()
    clear_text_file("data/users.txt")
    if request.method == "POST":
        #if request.form["playernum"] > 4:
            # Code about error too many players #
        #else:
            # below code #
        playernum = request.form["playernum"]
        return redirect("setup" + '/' + playernum)
    return render_template("index.html")
 
@app.route('/setup/<playernum>', methods=["GET", "POST"])
def username(playernum):
    # User(s) enter their desired usernames #
    instruct_num = str(leaderboard_len("data/leaderboard.json") + 1)
    if request.method == "POST":
        new_num = str(int(playernum) - 1)
        playernum = new_num
        if not check_in_file("data/users.txt", request.form["username"].title()):
            write_to_file("data/users.txt", request.form["username"].title() + "\n")
            add_to_leaderboard(request.form["username"].title())
        #else:
            #code about error message for duplicate usernames #
        
        if int(playernum) == 0:
                qnumber = str(leaderboard_len("data/leaderboard.json") - 1)
                return redirect(request.form["username"] + '/' + '1' + '/' + qnumber + '/' + '0')
        else:
            return redirect("setup" + '/' + playernum)
    return render_template("username.html", player=instruct_num)
 
@app.route('/<username>/<rnumber>/<qnumber>/<question>', methods=["GET", "POST"])
def riddle(username, rnumber, qnumber, question):
    # Main game page, questions are displayed, can be answered and wrong answers are displayed #
    incorrect_answers = print_content_in_list("data/incorrect_answers.txt")
    riddle = question_selector(question, rnumber)
    if request.method == "POST":
        return redirect('/' + username + '/' + rnumber + '/' + qnumber + '/' + question  + '/' + request.form["answer"])
    return render_template("riddle.html", username=username, incorrect_answers=incorrect_answers, riddle=riddle, rnumber= rnumber)
    
@app.route('/<username>/<rnumber>/<qnumber>/<question>/<answer>')
def send_answer(username, qnumber, answer, rnumber, question):
    # Create a new answer and redirect back to the riddle page
    if right_or_wrong(username, answer, qnumber, rnumber, question):
        qnumber = q_update(qnumber)
        question = question_update(question)
        if int(qnumber) == -1:
            rnumber = next_round(rnumber)
            qnumber = reset_turn(qnumber)
            username = next_player(username, qnumber)
        else:
            username = next_player(username, qnumber)
    else:
        qnumber = q_update(qnumber)
        if int(qnumber) == -1:
            qnumber = reset_turn(qnumber)
            username = next_player(username, qnumber)
        else:
            username = next_player(username, qnumber)
    if int(rnumber) > 3:
        return redirect("/leaderboard")
    return redirect('/' + username + '/' + rnumber + '/' + qnumber + '/' + question)

@app.route('/leaderboard', methods=["GET", "POST"])
def leaderboard():
    # Displays leaderboard and winner #
    number = 0
    winner = get_winner()
    leaderboard = order_leaderboard()
    return render_template("leaderboard.html", username=winner, leaderboard=leaderboard, number=number)

# ..................................Run Web App

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)