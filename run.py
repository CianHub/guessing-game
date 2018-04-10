# ..................................Set Up

import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
from operator import itemgetter
from functions import write_to_file, check_in_file, clear_text_file, print_content, check_riddle, store_incorrect_answers, check_answers, question_selector, increase_user_score, add_to_leaderboard, fix_leaderboard

app = Flask(__name__)

# ..................................Template Page Functions

@app.route('/', methods=["GET", "POST"])
def index():
    # If a user submits via the submit username button, a unique username is stored and user is redirected to their page, if username already exists user is logged in #
    if request.method == "POST":
        if check_in_file("data/users.txt", request.form["username"].title()):
            return redirect(request.form["username"] + '/' + '0')
        else:
            write_to_file("data/users.txt", request.form["username"].title() + "\n")
            add_to_leaderboard(request.form["username"].title())
            return redirect(request.form["username"] + '/' + '0')
    return render_template("index.html")
 
@app.route('/<username>/<qnumber>', methods=["GET", "POST"])
def user(username, qnumber):
    # Riddle Page #
    riddle = {}
    answers = print_content("data/incorrect_answers.txt")
    with open("data/riddles.json", "r") as content:
        data = json.load(content)
        for question in data:
            if question["number"] in qnumber:
                riddle = question["question"]
        if request.method == "POST":
            return redirect('/' + username + '/' + qnumber + '/' + request.form["answer"])
    return render_template("riddle.html", username=username, incorrect_answers=answers, riddle=riddle, qnumber=str(int(qnumber) + 1))

@app.route('/<username>/<qnumber>/<answer>')
def send_answer(username, qnumber, answer):
    # Create a new answer and redirect back to the riddle page
    if check_answers(username, answer, qnumber):
        new_q = str(int(qnumber) + 1)
        qnumber = new_q
    if int(qnumber) > 2:
        return redirect('/' + username + "/leaderboard")
    return redirect('/' + username + '/' + qnumber)

@app.route('/<username>/leaderboard', methods=["GET", "POST"])
def leaderboard(username):
    # Calls organised leaderboard and leaderboard.html page #
    number = 0
    leaderboard = fix_leaderboard()
    return render_template("leaderboard.html", username=username, leaderboard=leaderboard, number=number)

# ..................................Run Web App

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)