# ETproject
Final project for CS50x HarvardX course. As one of the prorposed projects i choose web application based on Flask framework. I though about making online word-based games. I already had actuall games implemented in code as part of MITx course. For this project i designed web sites and build user's web interface on top of engines i already had and joined it all in one monolithic app. Web app is written in Python(Flask), also uses HTML, CSS, jQuery, JS, SQLite3.

#### Description:
https://etproject.herokuapp.com

A webapp with word-based games. You can play hangman where you need to guesse a random word one letter at a time.
And you can play word game where you need to create word from given random letters. 
In word game you can compare yourself with computer or play against it.
Also you can keep score if you login. Registration is very simple, just enter a name.
Words will be saved in database and then a wordcloud will be generates if you visit News/Popular words page.



## app.py ##

App.py is the main file for the webapp, it contains all Flask settings, all the python module imports and 
all the routes to webpages. There is several slightly different routes here.
Simple render_template commands are given for pages index, about, news, login, logout pages.
Login also have an ability to create a table in data.db for each new username.
Logout pops a user from the session.
News will invoke data(list of words) from data.db and pass it as variable in render_template to news.html.
Then it will be processed with javascript to generate word cloud.
Function get_words() is imported from cloudofwords.py.

/hang handles get and post requests from user to play game of hangman. There is no interaction with database here.
It renders hang.html page. Data for the game is packed into JSON. So for the post request we use jsonify. Data can actually be seen in the console in web browser.
On the page we use jQuery for intercative user interface. There is no need to refresh page and game feels smoother.
In terms of design i kept it simple. User have an input form which is protected (can only import one letter, no numbers or symbols). Also there is "New Game" button, self explanatory. 
And two boxes: top one with information about game state and bottom one shows letters that are guessed.

/wordgame handles get and post requests from user to play word game. There is interaction with database here, if user logged in.
It renders wordgame.html page and sends two variables: user name for greeting on web page like "Hello, Username!" and scoreboard for generating a table.
Data for the game is packed into JSON. So for the post request we use jsonify. Data can actually be seen in the console in web browser.
On the page we use jQuery for intercative user interface. There is no need to refresh page and game feels smoother.
In terms of design i tried to keep it simple, but multiple things can be achived. With three buttons "New Game", "Replay Hand", "Computer Play"
user can play with herself or compare her result with computer on the same hand or play against the computer on different hands.
This is a bit advanced compared to hangman.

Initial code for this games can be found at "hangman.py" and "ps4a.py" and "ps4b.py". Originally it was problem sets from MITx 6001x course which
i adapted to this web app. I import some of the functions from said files and use them as a sort of external engines to keep my app.py a little bit cleaner.
For the same reason i use helpers.py and cloudofwords.py.  
All the words for games can be found in "/WordGame/words.txt"
"notes.py" is my dev notes files. Boring.

## data.db ##

Contains tables for each user to keep score for word game. Example of a table can be seen in query.sql.

## utility ##

"Procfile" is something needed to deploy on heroku. 
"runtime.txt" specifiec a version of Python to deploy on Heroku.
"requirements.txt" specifiec all of the dependencies for Python to deploy on Heroku.

## Folders ##

-cs50final - virtual environment folder

-flask_sessions - server utility

-static - css code, wordcloud code and jQuery

-templates - all html pages with some JS code on them for games and wordcloud generation.

