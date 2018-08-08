# ....Set Up

import os
import json
from datetime import datetime
import io
from operator import itemgetter
from random import randint

# ....Init Functions

def setup_leaderboard():
    # Initialises the leaderboard #
    
    data = {"leaderboard": []}
    write_json('data/leaderboard.json', data)
    json_decoded = load_json('data/leaderboard.json', 'r')
    if data == json_decoded:
        return True
        
def clear_global_leaderboard():
    # Initialises the global leaderboard #
    
    data = {"leaderboard": []}
    write_json('data/global_leaderboard.json', data)
    json_decoded = load_json('data/global_leaderboard.json', 'r')
    if data == json_decoded:
        return True

def init_riddles(filename):
    # Initialises the riddles file #
    
    data = load_json('data/riddles_backup.json', 'r')
    write_json(filename, data)
    json_decoded = load_json(filename, 'r')
    
    if data == json_decoded:
        return True
        
def init_game():
    # Initialises game #
    
    init_riddles("data/riddles.json")
    setup_leaderboard()
    clear_text_file("data/users.txt", "a")
    clear_text_file("data/incorrect_answers.txt", "a")

# ....General Functions

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

def check_leaderboard(data):
    # Check for data in leaderboard
    
    gameList = load_json('data/leaderboard.json', 'r')
    
    for x in range(len(gameList)):
        
        if data != gameList["leaderboard"][x]['username']:
            return False
            
        else:
            return True

def load_json(filename, letter):
    #Loads a JSON File #
    
    with open(filename, letter) as file:
        json_decoded = json.load(file)
        return json_decoded

def write_json(filename, data):
    # Writes to a JSON File #
    
    with open(filename, 'w') as file:
        json.dump(data, file)
        file.close()
        json_decoded = load_json(filename, 'r')
        
    if data == json_decoded:
        return True
    
def clear_text_file(filename, data):
    # Clears a text file #
    
    with open(filename, 'w') as f:
        f.write("")
        f.close()
        return check_in_file(filename, data)

def print_content_in_list(filename):
    # Prints content from a specified file #
    
    content = []
    with open(filename, "r") as file_content:
        content = file_content.readlines()
        return content

def random_number_generator_dependent(json_decoded):
    # Generates a random number  #
    
    next_question = randint(0, (len(json_decoded["riddles"]) - 1))
    question = str(next_question)
    return question

def random_number_generator():
    # Generates a random number from the range of the riddle file #
    
    next_question = randint(0, (riddle_len('data/riddles.json') - 1))
    question = str(next_question)
    return question

# ....Information Fetching Functions

def leaderboard_len(filename):
    # Gets the length of the leaderboard #
    
    json_decoded = load_json(filename, "r")
    return len(json_decoded['leaderboard'])

def riddle_len(filename):
    # Gets the length of the riddle file #
    
    json_decoded = load_json(filename, "r")
    return len(json_decoded['riddles'])

def get_player_name(position):
    # Get players name from ordered leaderboard #
    
    leaderboard = order_leaderboard()
    player_name = leaderboard[position]["username"]
    return player_name

def get_player_score(position):
    # Gets the players score from the ordered leaderboard #
    
    leaderboard = order_leaderboard()
    player_score = int(leaderboard[position]["score"])
    return player_score

def get_question_points(question):
    # Gets the players score from the ordered leaderboard #
    
    riddles = load_json('data/riddles.json', 'r')
    score = riddles['riddles'][int(question)]["points"]
    return score

# ....Round, Turn and Game Flow Functions

def next_round(rnumber):
    # Increments the rnumber #
    
    rnumber = str(int(rnumber) + 1)
    return rnumber

def reset_turn(qnumber):
    # Starts the turn cycle again #
    
    qnumber = str(leaderboard_len("data/leaderboard.json") - 1)
    return qnumber

def q_update(qnumber):
    # Decrements the qnumber #
    
    new_q = str(int(qnumber) - 1)
    qnumber = new_q
    return qnumber

def question_update(question):
    # removes previous question, increases question number #
    
    json_decoded = load_json('data/riddles.json', 'r')
    del json_decoded['riddles'][int(question)]
    next_question = random_number_generator_dependent(json_decoded)
    write_json('data/riddles.json', json_decoded)
    question = next_question
    clear_text_file("data/incorrect_answers.txt", 'a')
    return question

def question_selector(question):
    # Selects the  question #
    
    riddle = {}
    data = load_json('data/riddles.json', 'r')
    riddle = data['riddles'][int(question)]["question"]
    return riddle

def score_display(question):
    # Displays the points value of a question #
    
    score = 0
    data = load_json('data/riddles.json', 'r')
    score = data['riddles'][int(question)]["points"]
    return score

def turn_display(question):
    # Selects the turns value of a question #
    
    turns = 0
    data = load_json('data/riddles.json', 'r')
    turns = data['riddles'][int(question)]["turns"]
    return turns
                
def next_player(username, qnumber):
    # Moves the turn to the next player #
    
    json_decoded = load_json('data/leaderboard.json', 'r')
    
    for i in range(leaderboard_len('data/leaderboard.json')):
        
        if qnumber in json_decoded['leaderboard'][i]["qnumber"]:
            
            username = json_decoded['leaderboard'][i]["username"]
            return username

# ....Leaderboard Functions

def increase_user_score(username, question):
    # Increments a user's score #
    
    data = load_json('data/riddles.json', 'r')
    score = data['riddles'][int(question)]["points"]
    json_decoded = load_json("data/leaderboard.json", "r")
    
    for i in range(len(json_decoded['leaderboard'])):
        
        if username in json_decoded['leaderboard'][i]["username"]:
            
            json_decoded['leaderboard'][i]["score"] = json_decoded['leaderboard'][i]["score"] + score
            
            if write_json("data/leaderboard.json", json_decoded):
                
                return json_decoded['leaderboard'][i]["score"]

def increase_user_score_global(username, question):
    # Increments a user's score globally #
    
    data = load_json('data/riddles.json', 'r')
    score = data['riddles'][int(question)]["points"]
    json_decoded = load_json("data/global_leaderboard.json", "r")
    
    for i in range(len(json_decoded['leaderboard'])):
        
        if username in json_decoded['leaderboard'][i]["username"]:
            
            json_decoded['leaderboard'][i]["score"] = json_decoded['leaderboard'][i]["score"] + score
            
            if write_json("data/global_leaderboard.json", json_decoded):
                
                return json_decoded['leaderboard'][i]["score"]

def add_to_leaderboard(username, filename):
    # Adds new user and a starting score to leaderboard #
    
    json_decoded = load_json(filename, "r")
    
    data = { 
        "username": username, "score": 0, 
        "qnumber": str(len(json_decoded["leaderboard"])), 
        }
    json_decoded['leaderboard'].append(data)
    
    if write_json(filename, json_decoded):
        
        return True
        
def add_to_leaderboard_global(username, filename):
    # Adds new user and a starting score to global leaderboard #
    
    json_decoded = load_json(filename, "r")
    data = { 
        "username": username, "score": 0, 
        }
    json_decoded['leaderboard'].append(data)
    
    if write_json(filename, json_decoded):
        return True
            
def order_leaderboard_global():
    # Orders the global leaderboard according to score #
    
    json_decoded = load_json("data/global_leaderboard.json", "r")
    sorted_leaderboard = sorted(json_decoded['leaderboard'], 
    reverse=True, key=itemgetter("score"))
    return sorted_leaderboard

def order_leaderboard():
    # Orders the leaderboard according to score #
    
    json_decoded = load_json("data/leaderboard.json", "r")
    sorted_leaderboard = sorted(json_decoded['leaderboard'], 
    reverse=True, key=itemgetter("score"))
    return sorted_leaderboard

def decrement_score(question):
    # Reduces score value by 1 #
    
    json_decoded = load_json("data/riddles.json", "r")
    json_decoded['riddles'][int(question)]["points"] = json_decoded['riddles'][int(question)]["points"] - 1
    
    if write_json("data/riddles.json", json_decoded):
        return json_decoded['riddles'][int(question)]["points"]

def decrement_turns(question):
    # Reduces turns value of a question by 1 #
    
    json_decoded = load_json("data/riddles.json", "r")
    json_decoded['riddles'][int(question)]["turns"] = json_decoded['riddles'][int(question)]["turns"] - 1
    
    if write_json("data/riddles.json", json_decoded):
        return json_decoded['riddles'][int(question)]["turns"]
        
# ....Answer Checking Functions

def check_answer(answer, question):
    #Checks if the answer to the riddle is correct#
    
    data = load_json("data/riddles.json", "r")
    
    if answer.title() == data['riddles'][int(question)]["answer"]: 
            clear_text_file("data/incorrect_answers.txt" ,'a')
            return True
    else:
            return False
            
def store_incorrect_answers(username, answer):
    # write incorrect answers to the incorrect answer text file #
    
    write_to_file("data/incorrect_answers.txt", 
    "{0} - {1}\n".format(
        username.title(),
        answer))
    return check_in_file("data/incorrect_answers.txt", answer)

def right_or_wrong(username, answer, question):
    # Handles answer results #
    
    if check_answer(answer, question):
        
        increase_user_score(username, question)
        increase_user_score_global(username, question)
        return True
        
    else:
        decrement_score(question)
        decrement_turns(question)
        store_incorrect_answers(username, answer)