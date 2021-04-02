import sqlite3

from PyDictionary import PyDictionary
from hangman import choose_word
from flask import session


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# sql get

def dbGet(user_name):
    try:
        con = sqlite3.connect("data.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from user"+user_name+" ORDER BY ID DESC LIMIT 10;")
        table = cur.fetchall()
        con.close()
        return table
    except:
        print("Error retriving from Database")
        return None

def dbCreate(user_name):
    try:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE user"+user_name + " (id INTEGER,player TEXT,word TEXT,score INTEGER,totalScore INTEGER,date DATETIME,PRIMARY KEY(id));")
        con.close()
        return True
    except:
        print("Error creating a user_Database")
        return False
# sql insert 
def dbIns(data):
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("INSERT INTO user"+data[0]+" (player,word,score,totalScore,date) VALUES (?,?,?,?,?);", data)
        con.commit()
        con.close()
        return True
    except:
    
        print("Error inserting into Database")
        return False

def dbInsComputer(user_name, data):
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("INSERT INTO user"+user_name+" (player,word,score,totalScore,date) VALUES (?,?,?,?,?);", data)
        con.commit()
        con.close()
        return True
    except:
    
        print("Error inserting into Database")
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