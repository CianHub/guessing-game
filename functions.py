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
    
def print_content(filename):
    # Prints content from a specified file #
    content = []
    with open(filename, "r") as file_content:
        content = file_content.readlines()
    return content
 
# ..................................Riddle Game Functions

def check_riddle(answer, qnumber):
    #Checks if the answer to the riddle is correct#
    with open("data/riddles.json", "r") as riddles:
        content = json.load(riddles)
        for check in content:
            if check["answer"].title() in answer.title() and check["number"] in qnumber:
                clear_text_file("data/incorrect_answers.txt")
                return True
            elif check["answer"] not in answer:
                continue
            
def store_incorrect_answers(username, answer):
    # write incorrect answers to the incorrect answer text file #
    write_to_file("data/incorrect_answers.txt", "({0}) {1} - {2}\n".format(
        datetime.now().strftime('%H:%M:%S'),
        username.title(),
        answer))

def check_answers(username, answer, qnumber):
    # Check if answer is correct #
    if check_riddle(answer, qnumber):
        increase_user_score(username)
        return True
    else:
        store_incorrect_answers(username, answer)

def question_selector(qnumber):
    # Selects the current question #
    with open("data/riddles.json", "r") as content:
        data = json.load(content)
        for question in data:
            if question["number"] in qnumber:
                riddle = question["question"]
                return riddle

def increase_user_score(username):
    # Increases user score by 1 #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        for i in range(len(json_decoded['leaderboard'])):
            if username in json_decoded['leaderboard'][i]["username"]:
                json_decoded['leaderboard'][i]["score"] = json_decoded['leaderboard'][i]["score"] + 1
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)
        
def add_to_leaderboard(username):
    # Adds new users and a starting score to leaderboard #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        data = { "username": username, "score": 0}
        json_decoded['leaderboard'].append(data)
        with open("data/leaderboard.json", 'w') as new_file:
            json.dump(json_decoded, new_file)

def fix_leaderboard():
    # Rearranges leaderboard according to score #
    with open("data/leaderboard.json", "r") as json_file:
        json_decoded = json.load(json_file)
        sorted_leaderboard = sorted(json_decoded['leaderboard'], reverse=True, key=itemgetter("score"))
        print(sorted_leaderboard)
        return sorted_leaderboard
