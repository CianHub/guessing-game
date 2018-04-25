import os
import json
import io
from operator import itemgetter
import unittest

from functions import(
    write_to_file, check_in_file, clear_text_file,
    print_content_in_list, check_answer, store_incorrect_answers,
    right_or_wrong, question_selector, increase_user_score,
    add_to_leaderboard, order_leaderboard, setup_leaderboard,
    next_player, leaderboard_len, next_round, reset_turn, q_update,
    get_player_name, question_update, random_number_generator_dependent,
    init_riddles, get_player_score, random_number_generator, init_game,
    score_display, decrement_score, get_question_points, load_json, write_json, riddle_len
    )
 

class test_game(unittest.TestCase):
    
    # Test Suite #
      
    # ..................................Init Functions
    
    def test_setup_leaderboard(self):
        # Test if function returns True upon searching for what it just wrote in the file #
        self.assertEqual(setup_leaderboard(), True)
        
    def test_init_riddles(self):
        # Test if function returns True upon searching for a question in the file #
        self.assertEqual(init_riddles('data/riddles.json'), True)
    
    # ..................................General Functions
    
    def test_write_to_file(self):
        # Test if function writes to a txt file #
        self.assertEqual(write_to_file("data/users.txt", 'Test'.title()), True)
    
    def test_check_in_file(self):
        # Test if functions checks if data is in a txt file #
        write_to_file("data/users.txt", 'Test'.title())
        self.assertEqual(check_in_file("data/users.txt", 'Test'.title()), True)
        self.assertEqual(check_in_file("data/users.txt", '0'), False)
    
    def test_load_json(self):
        # Test that function loads JSON file #
        with open('data/riddles.json', 'r') as file:
            json_decoded = json.load(file)
            self.assertEqual(load_json('data/riddles.json', 'r'), json_decoded)
    
    def test_write_json(self):
        # Test that function writes to a JSON file #
        self.assertEqual(write_json('data/test.json', 'test'), True)
    
    def test_clear_text_file(self):
        # Test if function clears a txt file #
        write_to_file("data/users.txt", "data")
        self.assertEqual(clear_text_file("data/users.txt", 'data'), False)
    
    def test_print_content_in_list(self):
        # Test if function writes to a txt file #
        assert type(print_content_in_list("data/users.txt")) is list
    
    def test_random_number_generator_dependent(self):
        # Test if function returns a random number in str format #
        with open("data/riddles.json", "r") as json_file:
            json_decoded = json.load(json_file)
            assert type(random_number_generator_dependent(json_decoded)) is str
            assert type(int(random_number_generator_dependent(json_decoded))) is int
    
    def test_random_number_generator(self):
        # Test if function returns a random number in str format #
        assert type(random_number_generator()) is str
        assert type(int(random_number_generator())) is int
    
    # ....Information Fetching Functions
    
    def test_leaderboard_len(self):
        # Test if function returns length of the leaderboard in int format #
        assert type(leaderboard_len('data/leaderboard.json')) is int
    
    def test_riddle_len(self):
        # Test if function returns numbers of riddles in int format #
        assert type(riddle_len('data/riddles.json')) is int
    
    def test_get_player_name(self):
        # Test if function gets a players name #
        setup_leaderboard()
        add_to_leaderboard("Jason")
        add_to_leaderboard("Zebra")
        self.assertEqual(get_player_name(0), "Jason")
        self.assertEqual(get_player_name(1), "Zebra")
    
    def test_get_player_score(self):
        # Test if function gets a players name #
        init_game()
        add_to_leaderboard("Jason")
        add_to_leaderboard("Zebra")
        increase_user_score("Zebra", '2')
        self.assertEqual(get_player_score(1), 0)
        self.assertEqual(get_player_score(0), 10)
    
    def test_get_question_points(self):
        # Test if function gets a questions points value #
        init_game()
        decrement_score('2')
        self.assertEqual(get_question_points('1'), 10)
        self.assertEqual(get_question_points('2'), 9)
    
    # ....Round, Turn and Game Flow Functions
    
    def test_next_round(self):
        # Test if function returns the rnumber incremented by 1 in str format #
        assert type(next_round('0')) is str
        self.assertEqual((int(next_round(0))), 1)
    
    def test_reset_turn(self):
        # Test if function returns the leaderboard_len() decremnted by 1 in str format #
        init_game()
        add_to_leaderboard("Jason")
        add_to_leaderboard("Zebra")
        assert type(reset_turn('3')) is str
        self.assertEqual((int(reset_turn('2'))), 1)
    
    def test_q_update(self):
        # Test if function returns the qnumber decremnted by 1 in str format #
        init_game()
        assert type(q_update('3')) is str
        self.assertEqual((int(q_update('3'))), 2)
    
    def test_question_update(self):
        # Test if function returns a random number in str format #
        init_riddles('data/riddles.json')
        assert type(question_update("1")) is str
        assert type(int(question_update("1"))) is int
    
    def test_question_selector(self):
        # Test if function selects the correct question #
        self.assertEqual(question_selector('0'), "I have a ring, but no hands. I used to be plugged into the wall but now I follow you every where. What am I?")
    
    def test_score_display(self):
        # Test that function displays the questions points value #
        init_game()
        decrement_score('2')
        self.assertEqual(score_display('1'), 10)
        self.assertEqual(score_display('2'), 9)
    
    def test_next_player(self):
        # Test that function returns the next username #
        init_game()
        add_to_leaderboard("Jason")
        add_to_leaderboard("Zebra")
        self.assertEqual(next_player('Jason', '1'), 'Zebra')
    
    # ....Leaderboard Functions
    
    def test_increase_user_score(self):
        # Test if function increases the users score on the leaderboard #
        init_game()
        add_to_leaderboard("Petey")
        decrement_score('2')
        self.assertEqual(increase_user_score("Petey", '1'), 10)
        self.assertEqual(increase_user_score("Petey", '2'), 19)
    
    def test_add_to_leaderboard(self):
        # Test if function adds a new user to leaderboard #
        init_game()
        self.assertEqual(add_to_leaderboard('Jon'), True)
        self.assertEqual(add_to_leaderboard('Paul'), True)
        self.assertEqual(add_to_leaderboard('Sarah'), True)
    
    def test_order_leaderboard(self):
        # Test if function returns a rearranged version of the leaderboard list #
        init_game()
        add_to_leaderboard("Jamie")
        add_to_leaderboard("Petey")
        increase_user_score("Petey", '1')
        with open("data/leaderboard.json", "r") as json_file:
            loaded_json = json.load(json_file)
            original_leaderboard = loaded_json['leaderboard']
            assert type(order_leaderboard()) is list
            self.assertNotEqual(order_leaderboard(), original_leaderboard)
        
    def test_decrement_score(self):
        # Tests if function decrements the points value of a question #
        self.assertEqual(decrement_score('1'), 9)
        self.assertEqual(decrement_score('1'), 8)
    
    # ....Answer Checking Functions
    
    def test_check_answer(self):
        # Test if function checks if an answer is correct #
        init_game()
        self.assertEqual(check_answer("Telephone", '0'), True)
        self.assertEqual(check_answer("The wrong answer", '1'), False)
    
    def test_store_incorrect_answers(self):
        # Test if function stores incorrect answers #
        self.assertEqual(store_incorrect_answers("Test", 'The wrong answer'), True)
    
    def test_right_or_wrong(self):
        # Test if function checks if an answer is right or wrong #
        init_game()
        add_to_leaderboard("Jason")
        add_to_leaderboard("Paul")
        add_to_leaderboard("Eva")
        self.assertEqual(right_or_wrong("Jason","Telephone", '0'), True)
        self.assertEqual(right_or_wrong("Paul","The wrong answer", '2'), None)
        self.assertEqual(right_or_wrong("Eva","Fall", '1'), True)