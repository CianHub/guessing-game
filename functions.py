# ..................................Set Up

import os
import json
from datetime import datetime
import io
from operator import itemgetter

# ..................................General Functions

def write_to_file(filename, data):
    #Writes data to a specified file#
    with open(filename,"a") as file:
        file.writelines(data)
        file.close()
        return check_in_file(filename, data)

def check_in_file(filename, data):
    #Checks if data is in a specified file#
    with open(filename) as file:
        content = file.read()
        if data in content:
            return True
        else:
            return False
            
def clear_text_file(filename):
    # Clears a specified text file #
    with open(filename, 'w') as f:
        f.write("")
        f.close()
        return check_in_file(filename, "Test")
    
def print_content_in_list(filename):
    # Prints content from a specified file #
    content = []
    with open(filename, "r") as file_content:
        content = file_content.readlines()
        return content
 
# ..................................Riddle Game Functions

def check_answer(answer,rnumber, question):
    #Checks if the answer to the riddle is correct#
    with open("data/riddles.json", "r") as riddles:
        data = json.load(riddles)
        for i in range(len(data['riddles'])):
            if answer.title() == data['riddles'][i]["answer"] and question == data['riddles'][i]["number"]:
                clear_text_file("data/incorrect_answers.txt")
                return True
            elif data['riddles'][i]["answer"]  not in answer:
                continue
        
def store_incorrect_answers(username, answer):
    # write incorrect answers to the incorrect answer text file #
    write_to_file("data/incorrect_answers.txt", "({0}) {1} - {2}\n".format(
        datetime.now().strftime('%H:%M:%S'),
        username.title(),
        answer))
    return check_in_file("data/incorrect_answers.txt", answer)

def right_or_wrong(username, answer, qnumber, rnumber, question):
    # Handles answer results #
    if check_answer(answer, rnumber, question):
        increase_user_score(username)
        return True
    else:
        store_incorrect_answers(username, answer)

def next_player(username, qnumber):
    # Moves the turn to the next player #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        for i in range(len(json_decoded['leaderboard'])):
            if qnumber in json_decoded['leaderboard'][i]["qnumber"]:
                username = json_decoded['leaderboard'][i]["username"]
                return username
  
def question_selector(question, rnumber):
    # Selects the current question #
    riddle = {}
    with open("data/riddles.json", "r") as content:
        data = json.load(content)
        for i in range(len(data['riddles'])):
            if question == data['riddles'][i]["number"] and rnumber == data['riddles'][i]["round"]:
                riddle = data['riddles'][i]["question"]
                print (data['riddles'][i]["question"])
                return riddle
            
def increase_user_score(username):
    # Increments a user's score #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        for i in range(len(json_decoded['leaderboard'])):
            if username in json_decoded['leaderboard'][i]["username"]:
                json_decoded['leaderboard'][i]["score"] = json_decoded['leaderboard'][i]["score"] + 1
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
            return json_decoded['leaderboard'][i]["score"]

def setup_leaderboard():
    # Initialises the leaderboard #
        data = {"leaderboard": []}
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(data, new_file)
   
def add_to_leaderboard(username):
    # Adds new users and a starting score to leaderboard #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        data = { "username": username, "score": 0, "qnumber": str(len(json_decoded["leaderboard"]))}
        json_decoded['leaderboard'].append(data)
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
            new_file.close()
            return check_in_file("data/leaderboard.json", data["username"])

def order_leaderboard():
    # Orders the leaderboard according to score #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        sorted_leaderboard = sorted(json_decoded['leaderboard'], reverse=True, key=itemgetter("score"))
        return sorted_leaderboard
        
def leaderboard_len(leaderboard):
    # Gets the length of the leaderboard #
    with open(leaderboard, "r") as json_file:
        json_decoded = json.load(json_file)
        return len(json_decoded['leaderboard'])
        
def next_round(rnumber):
    # Increments the rnumber #
    rnumber = str(int(rnumber) + 1)
    return rnumber

def reset_turn(qnumber):
    # Starts the turn cycle again e.g. after everyone has a turn it is the first player's turn again #
    qnumber = str(leaderboard_len("data/leaderboard.json") - 1)
    return qnumber
    
def q_update(qnumber):
    # Decrements the qnumber #
    new_q = str(int(qnumber) - 1)
    qnumber = new_q
    return qnumber

def question_update(question):
    # Changes the current question number #
    next_question = str(int(question) + 1)
    question = next_question
    return question

def get_winner():
    # Gets the winner from the ordered leaderboard #
    leaderboard = order_leaderboard()
    winner = leaderboard[0]["username"]
    return winner


        