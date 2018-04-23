# RIDDLE-ME-THIS Guessing Game 

Riddle-Me-This is a web application game that asks players to guess the answer to a riddle. The player is presented with text that contains the riddle. Players enter their answer into a textarea and submit their answer using a form. If a player guesses correctly, they are redirected to the next riddle. If a player guesses incorrectly, their incorrect guess is stored and printed below the riddle. Multiple players can play an instance of the game at the same time. Users are identified by a unique username. At the end of each game a leaderboard is displayed that ranks top scores for all users.

## Features

The application has several features:

1. One to four players can chose their unique user name and compete to score points by answering riddles.
2. The game lasts three rounds, a round length is one turn per player.
3. Player scores are stored and displayed in a leaderboard when the game has ended.

## Technologies

The application was developed with Flask, Python3, HTML5, CSS3, JavaScript, JQuery and Bootstrap.

## Installation

<<<<<<< HEAD
1. Ensure Python3, pip and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder
5. Setup the virtualenv instance for the project and activate the virtualenv instance 
7. Install required packages from requirements.txt 
8. Run run.py 
=======
1. Download the respository from GitHub.
2. Install Python3 (Found Here: <https://www.python.org/downloads/>)
3. Install the pip and virtualenv packages (See here: <https://packaging.python.org/guides/installing-using-pip-and-virtualenv/>)
4. Go to the repository folder from step 1. ($ cd repositoryFolder)
5. Setup the virtualenv instance for the project ($ python3* -m virtualenv projectName)
6. Activate the virtualenv instance ($ . projectName/bin/activate on Mac/Linux or $ projectName\Scripts\activate on Windows)
7. Install required packages from requirements.txt (pip install -r requirements.txt)
8. Run run.py ($ python3 run.py)
>>>>>>> 4366681f994956e5fb12671be965e1cc07aac9c5

*Note: This is for Mac OS/Linux on Windows "python3" should be replaced with "py"

## Testing

### Automated Testing

In the development of this application testing almost entirely consisted of automated tests using the python unittest package. My approach to testing was to write my functions with testing in mind. This ensured that my functions were written to be "testable" and simplified as much as possible, while taking in parameters and returning measurable results, thus having a clear output to test.

### Test Driven Development

I utlised a TDD(Test Driven Development Approach) throughout much of the development of the application. This led to simpler, more readable code and accelerated the development. By having a clearly defined and testable end result, I found it an easier process to write my functions. The test_leaderboard_len('filename') function is a very simple function that was written in this manner, where being clearly able to test the ouput greatly sped up the process.

```
def test_leaderboard_len(self):
        # Test if function returns length of the leaderboard in int format #
        assert type(leaderboard_len('data/leaderboard.json')) is int
 ```

Similiarly while working on the increase_user_score(username) function, I found this approach beneficial as the function works in tandem with several others in particular those related to the leaderboard. Using TDD made it easier to isolate the entire process related to the function I was writing and better visualise what I was trying to achieve. E.g. In the test below I was able to isolate the process of adding a user to the leaderboard and increasing their score from start to finish without the distraction of the rest of the application.

```
def test_increase_user_score(self):
        # Test if function increases the users score on the leaderboard #
        # add_to_leaderboard initialises a new users score at 0, so new user Petey will have a score of 0 to start with #
        add_to_leaderboard("Petey")
        self.assertEqual(increase_user_score("Petey"), 1)
        self.assertGreater(increase_user_score('Petey'), 0)
        self.assertNotEqual(increase_user_score('Petey'), 0)
```

## Deployment

The application was deployed to Heroku and can be viewed at: <https://riddle-me-this-game.herokuapp.com/>
