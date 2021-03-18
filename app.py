from PyDictionary import PyDictionary

from ps4a import *
from ps4b import *

import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="verysecret"
# con = sqlite3.connect('data.db')
# cur = con.cursor()
# con.close()

# # Create table
# cur.execute('''CREATE TABLE stocks
#                (date text, trans text, symbol text, qty real, price real)''')

# # Insert a row of data
# cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# con.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # hand = request.args.get('hand')
        return render_template("index.html")
    if request.method == "POST":
        # usrInp = request.form.get("usrInp")
        # wordList = loadWords()
        # output = playHand(usrInp,wordList, HAND_SIZE, hand)
        
        # playGame(usrInp, wordList)

        return render_template("index.html", output = output)

@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/thru", methods=['GET', 'POST'])
def thru():
    wordList = loadWords()
    dictionary=PyDictionary()
    if request.method == 'GET':
        # hand = request.args.get('hand')
        return render_template("thru.html")
    if request.method == 'POST':
        userInp = request.form['userInp']
        if not userInp:
            out ="You send a blank form"
            mes =""
        else:
            HAND_SIZE = 6

            if userInp== 'n':
                hand = dealHand(HAND_SIZE)
                session["hand"] = hand
                session["hand_copy"] = hand.copy()
                totalscore = 0
                session['score'] = 0
                out = displayHand(hand)
                mes = "New Hand Dealt"
                return jsonify(out +"@"+ mes)
            
            elif userInp== 'r':
                hand = session['hand_copy']
                print("copy ", hand)
                session["hand"] = hand
                totalscore = 0
                session['score'] = 0
                out = displayHand(hand)
                mes = "Hand replayed"
                return jsonify(out +"@"+ mes)
            
            elif userInp == 'c':
                wordDict = getWordDict(wordList, HAND_SIZE)
                hand = session["hand"]
                totalscore = session['score']
                mes, hand, totalscore = compPlayHand(hand, wordList, HAND_SIZE, totalscore, wordDict)
                word = mes.split(" ")[1]
                meaning = dictionary.meaning(word)
                if meaning != None:
                    meaning= "Definition: " + str(list(meaning.values()))[2:-1]
                else:
                    meaning = ""
                print("computer plays hand ", hand)
                session['score'] = totalscore
                session["hand"] = hand
                out = displayHand(hand)
                return jsonify(out +"@"+ mes + "@" + meaning)

            else:
                hand = session["hand"]
                totalscore = session['score']
                mes, hand, totalscore = playHand(userInp,hand,wordList,HAND_SIZE, totalscore)
                session['score'] = totalscore
                session["hand"] = hand
                out = displayHand(hand)
                return jsonify(out +"@"+ mes)
        

if __name__ == "__main__":
    app.run(debug=True)    