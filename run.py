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
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)