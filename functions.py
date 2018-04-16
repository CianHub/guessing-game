# ..................................Set Up

import os
import json
from datetime import datetime
import io
from operator import itemgetter
from random import randint


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

def get_player_name(position):
    # Gets the players name from the ordered leaderboard #
    leaderboard = order_leaderboard()
    player_name = leaderboard[position]["username"]
    return player_name

def get_player_score(position):
    # Gets the players score from the ordered leaderboard #
    leaderboard = order_leaderboard()
    player_score = int(leaderboard[position]["score"])
    return player_score
    
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

def random_number_generator(json_decoded):
    # Generates a random number from the range of the copy of the riddle file #
    next_question = randint(0, (len(json_decoded["riddles"]) - 1))
    question = str(next_question)
    return question

def random_number_generator_init():
    # Generates a random number from the range of the riddle file #
    next_question = randint(0, (riddle_len('data/riddles.json') - 1))
    question = str(next_question)
    return question
    
def question_update(question):
    # Changes the current question number and removes previous question from selection #
    with open("data/riddles.json", "r") as json_file:
        json_decoded = json.load(json_file)
        for i in range(len(json_decoded['riddles'])):
            if question in json_decoded['riddles'][i]["number"]:
                del json_decoded['riddles'][i]
                next_question = random_number_generator(json_decoded)
                question = next_question
                with open("data/riddles.json", 'w') as new_file:
                    json.dump(json_decoded, new_file)
                    json_file.close
                    new_file.close
                    return question
       
def question_selector(question, rnumber):
    # Selects the corresponding question #
    riddle = {}
    with open("data/riddles.json", "r") as content:
        data = json.load(content)
        for i in range(len(data['riddles'])):
            if question == data['riddles'][i]["number"]:
                riddle = data['riddles'][i]["question"]
                return riddle

def init_riddles(filename):
    # Initialises the riddles file #
    data = {"riddles": 
        [{
            "number": "0",
            "question": "I have a ring, but no hands. I used to be plugged into the wall but now I follow you every where. What am I?",
            "answer": "Telephone"},{
            "number": "1",
            "question": "What season does Humpty Dumpty hate the most?",
            "answer": "Fall"
        },{
            "number": "2",
            "question": "I am black when clean and white when dirty. What am I?",
            "answer": "Blackboard"

        },{
            "number": "3",
            "question": "What runs around a house but does not move?",
            "answer": "Fence"

        },{
            "number": "4",
            "question": "Once you have it, you want to share it. Once you share it, you don't have it. What is it?",
            "answer": "Secret"

        },{
            "number": "5",
            "question": "I start with M and end with X. I have a never ending amount of letters. What am I?",
            "answer": "Mailbox"}, {
            "number": "6",
            "question": "What can elephants make that no other animals can make?",
            "answer": "Elephants"

        },{
            "number": "7",
            "question": "I have a head & no body, but I do have a tail. What am I?",
            "answer": "Coin"

        },{
            "number": "8",
            "question": "What do you call a bear without an ear?",
            "answer": "B"

        },{
            "number": "9",
            "question": "I can be made and I can be played. I can be cracked and I can be told. What am I?",
            "answer": "Joke"

        },{
            "number": "10",
            "question": "What has a bed but doesn't sleep and a mouth but never eats ? ",
            "answer" : "River"

        },{
            "number": "11",
            "question": "I am a container with no sides and no lid, yet golden treasure lays inside. What am I?",
            "answer": "Egg"},{
            "number": "12",
            "question": "Which letter of the alphabet contains the most water?",
            "answer": "C"

        },{
            "number": "13",
            "question": "What has a soul but doesn't live and a tongue but can't taste?",
            "answer": "Shoe"

        },{
            "number": "14",
            "question": "You buy me to eat, but never eat me. What am I?",
            "answer": "Silverware"

        },{
            "number": "15",
            "question": "What ends everything always?",
            "answer": "G"

        },{
            "number": "16",
            "question": "The maker doesn't want it, the buyer doesn't use it and the user doesn't know it. What is it?",
            "answer": "Coffin"

        },{
            "number": "17",
            "question": "You go at red and stop at green. What am I?",
            "answer": "Watermelon"

        }]}
    with open(filename, 'w') as new_file:
        json.dump(data, new_file)
        new_file.close()
        return check_in_file(filename, data["riddles"][0]["answer"])

def init_game():
    # Initialises game #
    init_riddles("data/riddles.json")
    setup_leaderboard()
    clear_text_file("data/users.txt")



    
    