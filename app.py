import sqlite3
import os
import json

from PyDictionary import PyDictionary
from ps4a import loadWords, dealHand, displayHand, playHand
from ps4b import getWordDict, compPlayHand
from hangman import hangman, isWordGuessed
from cloudofwords import get_words
from datetime import datetime, timezone
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from helpers import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key= os.environ['SECRET'] or "b'\xa5\xa9\x1e\x0e\t3\xa4\x18^\xba\x08\xf7\xb1\xd0\xadG'"

Session(app)

# main page
@app.route("/")
def index():
    return render_template("index.html")

# about info
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    try:
        session.pop('username', None)
        return render_template("logout.html")
    except:
        return render_template("logoutB.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        dbCreate(session['username'])
        return redirect(url_for('wordgame'))
    else:
        return render_template("login.html")


@app.route("/news")
def news():
    data = get_words()
    return render_template("news.html", data=data)


# game of HANGMAN
@app.route("/hang", methods=['GET', 'POST'])
def hang():
    # render page
    if request.method == 'GET':
        session['user'] = 'Human'
        return render_template("hang.html")
    # game
    else:
        try:
            # button new game pressed
            userInp = request.json['newgame']
        except:
            # if button wasn't pressed but letter was inputted
            try:
                userInp = request.form['userInp']
                if request.form['userInp'] and not request.json['newgame'] :
                    game = {}
                    game['message'] = "Press New Game"
                    game['guesses'] = ""
                    return jsonify(game)
            # some safeguarding
            except:
                print("Wrong User Input")

        # load 80+k words
        wordList = loadWords()

        # if button new game pressed
        if userInp== '1':

            # initiate game
            inpdata = new_hangman(userInp, wordList)

            # send info to user
            return jsonify(inpdata)
        
        # game variables
        mistakesMade = session['mistakesMade']
        guessed_letters = session['guessed_letters']
        secretword = session['secretword']
        
        # create dict for game engine which is in ps4 file's
        inpData = {'secretWord': secretword, 'userInp' : userInp, "guessed_letters" : guessed_letters, 'mistakesMade' : mistakesMade }
        print("INPUT: ", inpData)
        # send data and get result of game state
        game = hangman(inpData)
        print("\nGAME: ", game)
        # check if run out of letters
        if game['ranout'] == 1:
            meaning = getWordDefinition(secretword)
            game['message'] = game.get('message') + meaning
            return jsonify(game)

        # write state to session
        session['guessed_letters'] = game['guessed_letters']
        session['mistakesMade'] = game['mistakesMade']
        guessed_letters = game['guessed_letters']
        
        # check if word guessed
        if isWordGuessed(secretword, guessed_letters) == True:
            meaning = getWordDefinition(secretword)
            message = f"Congratulations, you won! {meaning}"
            game['message'] = message
            # game['guesses'] = message about how many guesses left
            game['guesses'] = ''
            date = datetime.now(timezone.utc)
            score = 0
            totalscore = 0
            try:
                user_name = session['username']
            except:
                user_name = 'Hangman'
            data = [user_name, secretword, score, totalscore, date]
            flag=dbIns(data)
        
            return jsonify(game)
        
        return jsonify(game)



# game of WORDGAME
@app.route("/wordgame", methods=['GET', 'POST'])
def wordgame():
    print("WORDGAME!")
    try:
        print("USER", session['username'])
    except:
        print("no user name")
    try:
        user_name = session['username']
    except:
        user_name = "Anonymous"

    if request.method == 'GET':
        scoreboard = dbGet(user_name)
        return render_template("wordgame.html", scoreboard=scoreboard, username=user_name)
    
    elif request.method == 'POST':

        try:
            # always check for new game first
            userInp = request.json['newgame']
        except:
            # otherwise check for user input
            userInp= request.form['userInp']  

        # global varibels 
        wordList = loadWords()
        dictionary=PyDictionary()
        HAND_SIZE = 8
        
        # new game
        if userInp== 'n':
            # get hand
            hand = dealHand(HAND_SIZE)

            # write variables
            session["hand"] = hand
            session["hand_copy"] = hand.copy()
            totalscore = 0
            session['score'] = 0
            out = displayHand(hand)
            mes = "New Hand Dealt"
            # talk to SQL
            scoreboard = dbGet(user_name)
            # send data to user
            return jsonify(game = out, message = mes, database = scoreboard )
        
        # replay game
        elif userInp== 'r':
            # get hand from session
            hand = session['hand_copy']
            # write variables
            session["hand"] = hand
            totalscore = 0
            session['score'] = 0
            out = displayHand(hand)
            mes = "Hand replayed"
            # talk to SQL
            data = dbGet(user_name)
            # send data to user
            return jsonify(game = out, message = mes, database = data )
        
        # computer
        elif userInp == 'c':
            #get variables:
            wordDict = getWordDict(wordList, HAND_SIZE)
            hand = session["hand"]
            totalscore = session['score']
            #play function
            mes, hand, totalscore, score, word = compPlayHand(hand, wordList, HAND_SIZE, totalscore, wordDict)
            if word != None:
                #meaning from dictionary:
                meaning = getWordDefinition(word)
                #get date time and write to database:
                date = datetime.now(timezone.utc)
                ai_name = 'Computer'
                data = [ai_name, word, score, totalscore, date]
                flag=dbInsComputer(user_name, data)
                if flag == False:
                    print("Data NOT inserted")
            else:
                word = ""
                meaning= ""

            #update variables:
            session['score'] = totalscore
            session["hand"] = hand
            out = displayHand(hand)

            #send json to client:
            data = dbGet(user_name)
            return jsonify(game = out, message = mes, database = data, definition = meaning)

        # user plays
        else:
            # get vars from session
            hand = session["hand"]
            totalscore = session['score']
            # send and receive data from game engine
            mes, hand, totalscore, score, out_word = playHand(userInp,hand,wordList,HAND_SIZE, totalscore, )
            # update variables
            session['score'] = totalscore
            session["hand"] = hand
            out = displayHand(hand)

            # insert into database and get definition
            if out_word != None:
                date = datetime.now(timezone.utc)
                try:
                    user_name = session['username']
                except:
                    user_name = "username"
                data = [user_name, out_word, score, totalscore, date]
                flag=dbIns(data)
                if flag == False:
                    print("Data NOT inserted")
                meaning = dictionary.meaning(out_word)
                if meaning != None:
                    meaning= filter("Definition: " + str(list(meaning.values()))[2:-1])
                else:
                    meaning = ""
            else:
                meaning = ""
            data = dbGet(user_name)
            # send info to user
            return jsonify(game = out, message = mes, database = data,definition = meaning )
       

if __name__ == "__main__":
    app.run(debug=False)    