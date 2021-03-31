import sqlite3

# #fetch as list
# con = sqlite3.connect('data.db')
# cur = con.cursor()
# con.execute("")
# cur.execute("select * from scoreboard")
# data = cur.fetchall()
# for row in data:
#     print(row[0:5])
# con.close()

# #fetch as dictionary
# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

# con = sqlite3.connect("data.db")
# con.row_factory = dict_factory
# cur = con.cursor()
# cur.execute("select * from scoreboard")
# print (cur.fetchall())
# con.close()

# def getInd(l):
#     return l[3]

# def announce(f):
#     def wrapper():
#         print("Let's Start")
#         f()
#         print("That's end")
#     return wrapper

# @announce
# def hello():
#     print("Hello")


# x = 3
# y = 4

# bar = lambda x, y: x ** y

# foo = lambda l : l[3]

# print (bar(x,y))


# WORDLIST_FILENAME = "WordGame/words.txt"

# def loadWords():
#     """
#     Returns a list of valid words. Words are strings of lowercase letters.
    
#     Depending on the size of the word list, this function may
#     take a while to finish.
#     """
#     print("Loading word list from file...")
#     # inFile: file
#     inFile = open(WORDLIST_FILENAME, 'r')
#     # wordList: list of strings
#     wordList = []
#     for line in inFile:
#         wordList.append(line.strip().lower())
#     print("  ", len(wordList), "words loaded.")
#     return wordList
# wordlist = loadWords()
# book = {}
# for word in wordlist:
#     x = len(word)
#     book[x] = book.get(x,0) + 1
# print("calculating")
# print(book)
# game['mistakesMade'] = 0
# game['welcome']
# game['guesses'] = (f"You have {guesses - mistakesMade} guesses left")
# game['guessed_letters']
# game['available_letters']
# game['guessed_word']
# game['message']
# game['mistakesMade']
# secretword = 'catch'
# from PyDictionary import PyDictionary
# dictionary=PyDictionary()
# meaning = dictionary.meaning(secretword)

# for m in meaning:
#     for n in meaning['Noun']:
#         print(n)
#     for v in meaning['Verb']:
#         print(v)
game ={}
meaning = ' meaning'
game['Message']= 'you lost'
game['ranout'] = 1
if game.get('ranout') == 1:
    game['Message'] = game.get('Message') + meaning
    print(game['Message'])

# print(meaning['verb'][0])
# print(meaning['adjective'][0])