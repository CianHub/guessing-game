import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

def write_to_file(filename, data):
    #Writes data to a specified file#
    with open(filename,"a") as file:
        file.writelines(data)

def check_in_file(filename, data):
    #Checks if data is in a specified file#
    with open(filename) as file:
        content = file.read()
        if data in content:
            return True
        else:
            return False
            
def print_content(filename):
    # Prints content from a specified file #
    content = []
    with open(filename, "r") as file_content:
        content = file_content.readlines()
    return content
        
@app.route('/', methods=["GET", "POST"])
def index():
    #If a user submits via the submit username button, a unique username is stored and user is redirected to their page, if username already exists user is logged in #
    if request.method == "POST":
        if check_in_file("data/users.txt", request.form["username"].title()):
            return redirect(request.form["username"])
        else:
            write_to_file("data/users.txt", request.form["username"].title() + "\n")
            return redirect(request.form["username"])
    return render_template("index.html")
 
def store_incorrect_answers(username, answer):
    # write incorrect answers to the incorrect answer text file #
    write_to_file("data/incorrect_answers.txt", "({0}) {1} - {2}\n".format(
        datetime.now().strftime('%H:%M:%S'),
        username.title(),
        answer))

def check_answers(username, answer):
    # Check if answer is incorrect and if so add the incorrect answer to the incorrect answer text file #
    if check_in_file("data/riddles.json", answer):
        print("correct")
    else:
        print("incorrect")
        store_incorrect_answers(username, answer)
        
@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    answers = print_content("data/incorrect_answers.txt")
    if request.method == "POST":
        return redirect('/' + username + '/' + request.form["answer"])
    return render_template("riddle.html", username=username, incorrect_answers=answers)

@app.route('/<username>/<answer>')
def send_answer(username, answer):
    """ Create a new answer and redirect back to the riddle page"""
    check_answers(username, answer )
    return redirect(username)
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)