from PyDictionary import PyDictionary


from ps4a import *
from ps4b import *
from hangman import *

from datetime import datetime, timezone
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="verysecret"

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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/hang", methods=['GET', 'POST'])
def hang():
    if request.method == 'GET':
        return render_template("hang.html")
    else:
        try:
            userInp = request.json['newgame']
        except:
            try:
                userInp = request.form['userInp']
            except:
                print("Wrong User Input")

        wordList = loadWords()
        if userInp== '1':
            guessed_letters = []
            mistakesMade = 0
            session['guessed_letters']= guessed_letters
            secretword = choose_word(wordList)
            session['secretword'] = secretword
            session['mistakesMade'] = mistakesMade
            welcome =f"Welcome to the game Hangman! I am thinking of a word that is {len(secretword)} letters long. You have {int(len(secretword) + 1)} guesses."
            
            inpdata = {'secretWord': secretword, 'userInp' : userInp, "guessed_letters" : guessed_letters, 'mistakesMade' : mistakesMade}
            inpdata['welcome'] = welcome
            return jsonify(inpdata)
        else:
            userInp = request.form['userInp']
        
        
            
        mistakesMade = session['mistakesMade']
        guessed_letters = session['guessed_letters']
        secretword = session['secretword']
        
        
        inpData = {'secretWord': secretword, 'userInp' : userInp, "guessed_letters" : guessed_letters, 'mistakesMade' : mistakesMade }
        
        game = hangman(inpData)
        session['guessed_letters'] = game['guessed_letters']
        session['mistakesMade'] = game['mistakesMade']
        
        guessed_letters = game['guessed_letters']
    #   game['guesses'] = message about how many guesses left
        if isWordGuessed(secretword, guessed_letters) == True:
            meaning = getWordDefinition(secretword)
            message = f"Congratulations, you won! {meaning}"
            game['message'] = message
            game['guesses'] = ''
            return jsonify(game)
        if game['ranout'] == 1:
            meaning = getWordDefinition(secretword)
            game['message'] = game.get('message') + meaning
        return jsonify(game)

def getWordDefinition(secretword):
    dictionary=PyDictionary()
    meaning = dictionary.meaning(secretword)
    if meaning != None:
        meaning= filter(" Definition: " + str(list(meaning.values()))[2:-1])
    else:
        meaning = ""
    return meaning


@app.route("/wordgame", methods=['GET', 'POST'])
def wordgame():


    if request.method == 'GET':
        scoreboard = dbGet()
        return render_template("wordgame.html", scoreboard=scoreboard)
    elif request.method == 'POST':
        try:
            userInp = request.json['newgame']
        except:
            userInp= request.form['userInp']     
        wordList = loadWords()
        dictionary=PyDictionary()
        HAND_SIZE = 8
        if userInp== 'n':
            hand = dealHand(HAND_SIZE)
            session["hand"] = hand
            session["hand_copy"] = hand.copy()
            totalscore = 0
            session['score'] = 0
            out = displayHand(hand)
            mes = "New Hand Dealt"
            scoreboard = dbGet()
            data = dbGet()
            return jsonify(game = out, message = mes, database = data )
        
        elif userInp== 'r':
            hand = session['hand_copy']
            print("copy ", hand)
            session["hand"] = hand
            totalscore = 0
            session['score'] = 0
            out = displayHand(hand)
            mes = "Hand replayed"
            data = dbGet()
            return jsonify(game = out, message = mes, database = data )
        
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

            print("computer plays hand ", hand)
            #update variables:
            session['score'] = totalscore
            session["hand"] = hand
            out = displayHand(hand)

            #send json to client:
            data = dbGet()
            return jsonify(game = out, message = mes, database = data, definition = meaning)

        else:
            hand = session["hand"]
            totalscore = session['score']
            mes, hand, totalscore, score, out_word = playHand(userInp,hand,wordList,HAND_SIZE, totalscore, )
            session['score'] = totalscore
            session["hand"] = hand
            out = displayHand(hand)
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
            return jsonify(game = out, message = mes, database = data,definition = meaning )
       

if __name__ == "__main__":
    app.run(debug=True)    