import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

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

def check_riddle(answer, qnumber):
    #Checks if the answer to the riddle is correct#
    with open("data/riddles.json", "r") as riddles:
        
        content = json.load(riddles)
        for check in content:
            print qnumber
            if check["answer"] in answer and check["number"] in qnumber:
                print check["answer"]
                return True
            elif check["answer"] not in answer:
                print check["answer"]
                continue
                return False 
            
def print_content(filename):
    # Prints content from a specified file #
    content = []
    with open(filename, "r") as file_content:
        content = file_content.readlines()
    return content

def write_to_json(filename, user):
    data = {"name": user, "score": 0} 
    with io.open(filename, 'a', encoding='utf8') as outfile:
        str_ = json.dumps(data,indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False) 
        outfile.write(to_unicode(str_))
    
@app.route('/', methods=["GET", "POST"])
def index():
    # If a user submits via the submit username button, a unique username is stored and user is redirected to their page, if username already exists user is logged in #
    if request.method == "POST":
        if check_in_file("data/users.txt", request.form["username"].title()):
            return redirect(request.form["username"] + '/' + '0')
        else:
            write_to_file("data/users.txt", request.form["username"].title() + "\n")
            write_to_json("data/leaderboard.json", request.form["username"].title() )
            return redirect(request.form["username"] + '/' + '0')
    return render_template("index.html")
 
def store_incorrect_answers(username, answer):
    # write incorrect answers to the incorrect answer text file #
    write_to_file("data/incorrect_answers.txt", "({0}) {1} - {2}\n".format(
        datetime.now().strftime('%H:%M:%S'),
        username.title(),
        answer))

def check_answers(username, answer, qnumber):
    # Check if answer is incorrect and if so add the incorrect answer to the incorrect answer text file #
    if check_riddle(answer, qnumber):
        print("correct")
        return True
    else:
        print("incorrect")
        store_incorrect_answers(username, answer)
        
@app.route('/<username>/<qnumber>', methods=["GET", "POST"])
def user(username, qnumber):
    riddle = {}
    answers = print_content("data/incorrect_answers.txt")
    
    with open("data/riddles.json", "r") as content:
        data = json.load(content)
        for question in data:
            if question["number"] in qnumber:
                riddle = question["question"]
        
        if request.method == "POST":
            return redirect('/' + username + '/' + qnumber + '/' + request.form["answer"])
            
    return render_template("riddle.html", username=username, incorrect_answers=answers, riddle=riddle)

@app.route('/<username>/<qnumber>/<answer>')
def send_answer(username, qnumber, answer):
    """ Create a new answer and redirect back to the riddle page"""
    if check_answers(username, answer, qnumber):
        new_q = str(int(qnumber) + 1)
        qnumber = new_q
    if int(qnumber) > 2:
        return render_template("leaderboard.html")
        
    return redirect('/' + username + '/' + qnumber)
 
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)