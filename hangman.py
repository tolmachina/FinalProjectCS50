# Hangman Game from MITx
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "WordGame/words.txt"


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program



def isWordGuessed(secretWord, guessed_letters):
    '''
    secretWord: string, the word the user is guessing; assumes all letters are
      lowercase
    guessed_letters: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secretWord are in guessed_letters;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secretWord = list(secretWord)
    count = 0
    for i in secretWord:
      if i in guessed_letters:
        count += 1
    if count == len(secretWord):
        return True
    else:
        return False
 

def getGuessedWord(secretWord, guessed_letters):
    '''
    secretWord: string, the word the user is guessing
    guessed_letters: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secretWord have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    result = ''
    secretWord = list(secretWord)
    for c in secretWord:
      if c in guessed_letters:
        result = result + c
      else:
        result = result + '_ '
    return result
    # secretWord = 'apple'
    # guessed_letters = ['e', 'i', 'k', 'p', 'r', 's'] 
    # print(getGuessedWord(secretWord, guessed_letters)) '_ pp_ e'



def getAvailableLetters(guessed_letters):
    '''
    guessed_letters: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    result = list(string.ascii_lowercase)
    for i in guessed_letters:
        if i in result:
            result.remove(i)
    str1 =''.join(result)
    return str1 
    # FILL IN YOUR CODE HERE AND DELETE "pass"
   

def unique_letters(secretWord):
  '''
  Input: str secret word
  Output: integer number of unique letters in word
  '''
  result = len(set(secretWord))
  return result    
    

def hangman(inpData):
    '''
    secretWord: string, the secret word to guess.
   
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secretWord contains and how many guesses s/he starts with.
   
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    '''

    '''
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    '''
    '''
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    game = {}
    game['ranout'] = 0
    secretWord=inpData['secretWord']
    userInp=inpData['userInp']
    guessed_letters=inpData['guessed_letters']
    mistakesMade =inpData['mistakesMade']
    game['mistakesMade'] = mistakesMade
    guesses = int(len(secretWord) + 1)
    available_letters = ''.join(getAvailableLetters(guessed_letters))
    guessed_word = getGuessedWord(secretWord, guessed_letters)
    user_letter = userInp.lower()
    
    # the game begins

    game['guesses'] = (f"You have {guesses - mistakesMade} guesses left")
    
    # check if no more guesses
    if guesses - mistakesMade < 1:
      print("NO MORE LETTERS")
      message = (f"Sorry, you ran out of guesses. The word was {secretWord}.")
      game['ranout'] = 1
      game['message'] = message
      game['guesses'] = ""
      return game
    
    if user_letter.isalpha() == False:
      mistakesMade += 1
      message = ('Oops! That letter is not in my word. ')
      game['message'] = message
      game['mistakesMade'] = mistakesMade

    elif user_letter in guessed_letters:
      message = ("Oops! You've already guessed that letter.")
      game['message'] = message
  
    guessed_letters.append(user_letter)
    game['guessed_letters'] = guessed_letters
    available_letters = getAvailableLetters(guessed_letters)
    game['available_letters'] = available_letters
    guessed_word = getGuessedWord(secretWord, guessed_letters)
    game['guessed_word'] = guessed_word

    if user_letter in secretWord:
      message = ("Good guess!")
      game['message'] = message

    else:
      message = ("Oops! That letter is not in my word.")
      game['message'] = message
      mistakesMade += 1
      game['mistakesMade'] = mistakesMade
    
    return game