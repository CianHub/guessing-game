import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


def write_to_file(filename, data):
    """Handle the process of writing data to txt file"""
    with open(filename,"a") as file:
        file.writelines(data)
    

@app.route('/', methods=["GET", "POST"])
def index():
    #If a user submits via the submit
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")
    
def add_answers(username, answer):
    """Add answers to the `answer text file"""
    write_to_file("data/incorrect_answers.txt", "({0}) {1} - {2}\n".format(
        datetime.now().strftime('%H:%M:%S'),
        username.title(),
        answer))

def print_incorrect_answers():
    answers = []
    with open("data/incorrect_answers.txt", "r") as incorrect_answers:
        answers = incorrect_answers.readlines()
    return answers

@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    """Display riddle answers"""
    answers = print_incorrect_answers()
    if request.method == "POST":
        return redirect('/' + username + '/' + request.form["answer"])
    return render_template("riddle.html", username=username, incorrect_answers=answers)

@app.route('/<username>/<answer>')
def send_answer(username, answer):
    """ Create a new answer and redirect back to the riddle page"""
    add_answers(username, answer)
    return redirect(username)


app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)