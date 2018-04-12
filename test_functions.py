from functions import write_to_file, check_in_file, clear_text_file, print_content_in_list, check_answer, store_incorrect_answers, right_or_wrong, question_selector, increase_user_score, add_to_leaderboard, fix_leaderboard
import unittest 
import json
import os
import json
from flask import Flask, redirect, render_template, request

class test_game(unittest.TestCase):
    
    # Test Suite #
    
    def test_clear_text_file(self):
        # Test if function clears a txt file #
        self.assertEqual(clear_text_file("data/users.txt"), False)
        
    def test_write_to_file(self):
        # Test if function writes to a txt file #
        self.assertEqual(write_to_file("data/users.txt", 'Test'.title()), True)
    
    def test_check_in_file(self):
        # Test if functions checks if data is in a txt file #
        write_to_file("data/users.txt", 'Test'.title())
        self.assertEqual(check_in_file("data/users.txt", 'Test'.title()), True)
        self.assertEqual(check_in_file("data/users.txt", '0'), False)
    
    def test_print_content_in_lis(self):
        # Test if function writes to a txt file #
        assert type(print_content_in_list("data/users.txt")) is list
    
    def test_check_answer(self):
        # Test if function checks if an answer is correct #
        self.assertEqual(check_answer("The first answer", '0'), True)
        self.assertEqual(check_answer("The wrong answer", '1'), None)
    
    def test_store_incorrect_answers(self):
        # Test if function stores incorrect answers #
        self.assertEqual(store_incorrect_answers("Test", 'The wrong answer'), True)
    
    def test_right_or_wrong(self):
        # Test if function checks if an answer is right or wrong #
        self.assertEqual(right_or_wrong("Jason","The first answer", '0'), True)
        self.assertEqual(right_or_wrong("Paul","The wrong answer", '2'), None)
        self.assertEqual(right_or_wrong("Eva","The second answer", '1'), True)
    
    def test_question_selector(self):
        # Test if function selects the correct question #
        assert type(question_selector("0")) is str
        self.assertEqual(question_selector('15'), None)
        assert type(question_selector("2")) is str
        self.assertEqual(question_selector('F'), None)
    
    def test_add_to_leaderboard(self):
        # Test if function adds a new user and their score to leaderboard #
        self.assertEqual(add_to_leaderboard('Jon'), True)
        self.assertEqual(add_to_leaderboard('Paul'), True)
        self.assertEqual(add_to_leaderboard('Sarah'), True)
    
    def test_increase_user_score(self):
        # Test if function increases the users score on the leaderboard #
        # add_to_leaderboard initialises a new users score at 0, so new user Petey will have a score of 0 to start with #
        add_to_leaderboard("Petey")
        self.assertGreater(increase_user_score('Petey'), 0)
        self.assertNotEqual(increase_user_score('Petey'), 0)
    
    def test_fix_leaderboard(self):
        # Test if function returns a rearranged version of the leaderboard list #
        with open("data/leaderboard.json", "r") as json_file:
            loaded_json = json.load(json_file)
            original_leaderboard = loaded_json['leaderboard']
            assert type(fix_leaderboard()) is list
            self.assertNotEqual(fix_leaderboard(), original_leaderboard)
 

       