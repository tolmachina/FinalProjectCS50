from PyDictionary import PyDictionary


from ps4a import loadWords, dealHand, displayHand, playHand
from ps4b import getWordDict, compPlayHand
from hangman import hangman, choose_word, isWordGuessed

from datetime import datetime, timezone
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="verysecret"

Session(app)




#data = [(Player, Word, Score, totalscore, date)]
#helper function for sql
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# sql get
def dbGet():
    try:
        con = sqlite3.connect("data.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from scoreboard  ORDER BY ID DESC LIMIT 10")
        table = cur.fetchall()
        con.close()
        return table
    except:
        print("Error Connecting to Database")
        return None
    # Create table
    # cur.execute('''CREATE TABLE stocks
    #                (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    # con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    # 

# sql insert 
def dbIns(data):
    try:
        con = sqlite3.connect('data.db')
        con.executemany("INSERT INTO scoreboard(player,word,score,totalScore,date) VALUES (?,?,?,?,?)", data)
        con.commit()
        con.close()
        return True
    except:
        print("Error Connecting to Database")
        return False

# text filter for definitions
def filter(string):
    grid = "[{}]<>()"
    result = ""
    for s in string:
        if s not in grid:
            result += s
    return result

# using PyDict for word definitions
def getWordDefinition(secretword):
    
    dictionary=PyDictionary()
    meaning = dictionary.meaning(secretword)
    if meaning != None:
        meaning= filter(" Definition: " + str(list(meaning.values()))[2:-1])
    else:
        meaning = ""
    return meaning

# helper for hangman
def new_hangman(userInp, wordList):
    """
    Starts the game of hangman
    Returns Dict
    """
    guessed_letters = []
    mistakesMade = 0
    session['mistakesMade'] = mistakesMade
    session['guessed_letters']= guessed_letters
    
    secretword = choose_word(wordList)
    session['secretword'] = secretword
    
    welcome =f"Welcome to the game Hangman! I am thinking of a word that is {len(secretword)} letters long. You have {int(len(secretword) + 1)} guesses."
    
    inpdata = {'secretWord': secretword, 'userInp' : userInp, "guessed_letters" : guessed_letters, 'mistakesMade' : mistakesMade}
    inpdata['welcome'] = welcome
    return inpdata

# main page
@app.route("/")
def index():
    return render_template("index.html")

# about info
@app.route("/about")
def about():
    return render_template("about.html")

# game of HANGMAN
@app.route("/hang", methods=['GET', 'POST'])
def hang():
    # render page
    if request.method == 'GET':
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
                if userInp:
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
        
        # send data and get result of game state
        game = hangman(inpData)
        
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
            return jsonify(game)
        
        # if run out of letters
        elif game['ranout'] == 1:
            meaning = getWordDefinition(secretword)
            game['message'] = game.get('message') + meaning
        return jsonify(game)


# game of WORDGAME
@app.route("/wordgame", methods=['GET', 'POST'])
def wordgame():
    if request.method == 'GET':
        scoreboard = dbGet()
        return render_template("wordgame.html", scoreboard=scoreboard)
    
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
            scoreboard = dbGet()
            data = dbGet()
            # send data to user
            return jsonify(game = out, message = mes, database = data )
        
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
            data = dbGet()
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
            #meaning from dictionary:
            if word != None:
                meaning = getWordDefinition(secretword)
            
                #get date time and write to database:
                date = datetime.now(timezone.utc)
                data = [("Computer", word, score, totalscore, date)]
                flag=dbIns(data)
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
            data = dbGet()
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
                data = [("username", out_word, score, totalscore, date)]
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
            data = dbGet()
            # send info to user
            return jsonify(game = out, message = mes, database = data,definition = meaning )
       

@app.route("/news")
def news():
    return render_template("news.html")

if __name__ == "__main__":
    app.run(debug=True)    