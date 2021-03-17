from ps4a import playGame
from ps4a import HAND_SIZE, dealHand
from ps4a import *
from ps4b import *

from cs50 import SQL
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
# db = SQL("sqlite:///data.db")

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

totalscore = 0


@app.route("/thru", methods=['GET', 'POST'])
def thru():
    wordList = loadWords()

    if request.method == 'GET':
        # hand = request.args.get('hand')
        return render_template("thru.html")
    if request.method == 'POST':
        userInp = request.form['userInp']
        if not userInp:
            out ="You send a blank form"
            mes =""
        else:
            if userInp== 'n':
                hand = dealHand(HAND_SIZE)
                session["hand"] = hand
                totalscore = 0
                session['score'] = 0
                out = displayHand(hand)
                mes = "New Hand Dealt"
            # if userInp == 'c':
            #     hand = dealHand(HAND_SIZE)
            #     session["hand"] = hand
            #     totalscore = 0
            #     session['score'] = 0
            #     out = displayHand(hand)
            #     mes = "New Hand Dealt"
            #     mes, hand, totalscore = compPlayHand(hand, wordList, HAND_SIZE, totalScore)


            else:
                hand = session["hand"]
                totalscore = session['score']
                mes, hand, totalscore = playHand(userInp,hand,wordList,HAND_SIZE, totalscore)
                session['score'] = totalscore
                session["hand"] = hand
                out = displayHand(hand)
                
        return jsonify(out +" "+ mes)

if __name__ == "__main__":
    app.run(debug=True)    