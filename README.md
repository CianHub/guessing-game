# RIDDLE-ME-THIS Guessing Game

Riddle-Me-This is a web application game that asks players to guess the answer to a riddle. The player is presented with text that contains the riddle. Players enter their answer into a textarea and submit their answer using a form. If a player guesses correctly, they are redirected to the next riddle. If a player guesses incorrectly, their incorrect guess is stored and printed below the riddle. 

Multiple players can play an instance of the game at the same time. Users are identified by a unique username. At the end of each game a leaderboard is displayed that ranks top scores for all users.
 
## UX

### User Stories

Before beginning development on the site, several user stories were created to determine who a visitor to the site could be and what they might want from the site:

- "As a fan of riddles, I want to be able to jump into a quick riddle game on my device and see how I do in relation to other users."

- "As a vistor to the website, I want to play a game with my friends which we can easily understand, compete against each other in and see how we compare."

### Design

The application utilises a minimal, responsive design, mainly consisting of a text input field, two buttons and the information relating to the current screen. This convention is altered on the leaderboard screen where a table is used to display the leaderboard.

The styling of the application was inspired by a classroom aesthetic, in order to emphasise on the quiz aspect of the game. This was implememeted using a blackboard background image and a chalky handwritten font ([squeaky chalk sound](https://www.1001fonts.com/squeaky-chalk-sound-font.html))

## Features

The game has several features:

    1. One to four players can chose their unique user name and compete to score points by answering riddles.
    2. The game lasts five rounds, a round length is one turn per player.
    3. A player has three guesses per question, with each wrong answer deducting a point from the questions point value.
    4. Player scores are stored and displayed in a leaderboard when the game has ended

## Technologies Used

- [HTML](https://www.w3.org/)
    - The project uses **HTML** to create the website.

- [CSS](https://www.w3.org/)
    - The project uses **CSS** to style the website.

- [Bootstrap](https://getbootstrap.com/docs/3.3/)
    - The project uses **Bootstrap** to style the page and user experience.

- [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript)
    - The project uses **JavaScript** to use Bootstrap functions.

- [JQuery](https://jquery.com/)
    - The project uses **JQuery** to manipulate the DOM with Bootstrap functionality.

- [Python](https://www.python.org/)
    - The project uses **Python** to write the games logic and manipulate data.

- [Flask](http://flask.pocoo.org/)
    - The project uses **Flask** for the websites backend (server, load jinja2 templates etc.). 

## Testing

To run tests, in the CLI enter:
```
$ python -m unittest discover
``` 
### Automated Testing

In the development of this application testing almost entirely consisted of automated tests using the python unittest package. The approach to testing was to write the functions with testing in mind. This ensured that the functions were written to be "testable" and simplified as much as possible, while taking in parameters and returning measurable results, thus having a clear output to test.

### Test Driven Development

The project utlised a TDD(Test Driven Development Approach) throughout much of it's development. This led to simpler, more readable code and accelerated the development by having a clearly defined and testable end result. 

The test_leaderboard_len('filename') function is a very simple function that was written in this manner, where being clearly able to test the ouput greatly sped up the process.

```
def test_leaderboard_len(self):
        # Test if function returns length of the leaderboard in int format #
        assert type(leaderboard_len('data/leaderboard.json')) is int
 ```

Similiarly while working on the increase_user_score(username) function, I found this approach beneficial as the function works with several other functions also related to the leaderboard. Using TDD made it easier to isolate the process related to the function I was writing and better visualise what I was trying to achieve. E.g. In the test below I was able to isolate the process of adding a user to the leaderboard and increasing their score from start to finish from the rest of the application.

```
def test_increase_user_score(self):
        # Test if function increases the users score on the leaderboard #
        add_to_leaderboard("Petey")
        self.assertEqual(increase_user_score("Petey"), 1)
        self.assertGreater(increase_user_score('Petey'), 0)
        self.assertNotEqual(increase_user_score('Petey'), 0)
```

## Deployment

This project was deployed to Heroku. As this project does not require any sensitive data or have any similar requirements, it's deployment was quite simple. The IP and PORT was set in Heroku's config vars section and a Procfile was added to the repository.

 The Project can be viewed at: <https://riddle-me-this-game.herokuapp.com/>

## Installation

1. Ensure Python3, pip and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder
5. Setup the virtualenv instance for the project and activate the virtualenv instance 
7. Install required packages from requirements.txt 
8. Run run.py 

## Credits

### Acknowledgements

- The riddles in this project were copied from [Riddles.fyi](https://riddles.fyi/)
- The font used in this project can be found at [squeaky chalk sound font](https://www.1001fonts.com/squeaky-chalk-sound-font.html)
