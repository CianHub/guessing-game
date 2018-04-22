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
    with open("data/leaderboard.json", 'w') as new_file:
        json.dump(data, new_file)

def init_riddles(filename):
    # Initialises the riddles file #
    data = load_json('data/riddles_backup.json', 'r')
    if write_json('data/riddles.json', data):
        return True
        

def init_game():
    # Initialises game #
    init_riddles("data/riddles.json")
    setup_leaderboard()
    clear_text_file("data/users.txt")
    clear_text_file("data/incorrect_answers.txt")

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

def load_json(filename, letter):
    #Loads a JSON File #
    with open(filename, letter) as file:
        json_decoded = json.load(file)
        return json_decoded

def write_json(filename, data):
    # Writes to a JSON File #
    with open(filename, 'w') as file:
        json.dump(data, file)
        file.close
        if data == file:
            return True

def open_file(filename, letter):
    # Opens a File #
    with open(filename, letter) as file:
        return file
        
def clear_text_file(filename):
    # Clears a text file #
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
    with open(filename, "r") as json_file:
        json_decoded = json.load(json_file)
        return len(json_decoded['leaderboard'])

def riddle_len(filename):
    # Gets the length of the riddle file #
    with open(filename, "r") as json_file:
        json_decoded = json.load(json_file)
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
    qnumber = str(leaderboard_len
    ("data/leaderboard.json") - 1)
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
    clear_text_file("data/incorrect_answers.txt")
    return question

def question_selector(question):
    # Selects the  question #
    riddle = {}
    data = load_json('data/riddles.json', 'r')
    riddle = data['riddles'][int(question)]["question"]
    return riddle

def score_display(question):
    # Selects the  question #
    score = 0
    data = load_json('data/riddles.json', 'r')
    score = data['riddles'][int(question)]["points"]
    return score
                
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
    print(score)

    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        for i in range(len(json_decoded['leaderboard'])):
            if username in json_decoded['leaderboard'][i]["username"]:
                json_decoded['leaderboard'][i]["score"] = json_decoded['leaderboard'][i]["score"] + score
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
            return json_decoded['leaderboard'][i]["score"]

def add_to_leaderboard(username):
    # Adds new user and a starting score to leaderboard #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        data = { 
            "username": username, "score": 0, 
        "qnumber": str(len(json_decoded["leaderboard"]))
        }
        json_decoded['leaderboard'].append(data)
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
            new_file.close()
            return check_in_file("data/leaderboard.json", 
            data["username"])

def order_leaderboard():
    # Orders the leaderboard according to score #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        sorted_leaderboard = sorted(json_decoded['leaderboard'], 
        reverse=True, key=itemgetter("score"))
        return sorted_leaderboard

def decrement_score(question):
    with open("data/riddles.json", "r") as json_file:
        json_decoded = json.load(json_file)
        json_decoded['riddles'][int(question)]["points"] = json_decoded['riddles'][int(question)]["points"] - 1
        with open("data/riddles.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
            return json_decoded['riddles'][int(question)]["points"]
    
# ....Answer Checking Functions

def check_answer(answer, question):
    #Checks if the answer to the riddle is correct#
    with open("data/riddles.json", "r") as riddles:
        data = json.load(riddles)
        if answer.title() == data['riddles'][int(question)]["answer"]: 
            clear_text_file("data/incorrect_answers.txt")
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
        return True
    else:
        decrement_score(question)
        store_incorrect_answers(username, answer)