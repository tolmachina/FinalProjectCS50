from ps4a import *
import time



# EVGENY TOLMACHEV
#
# Computer chooses a word
#
#
def compChooseWord(hand, wordDict, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    # Create a new variable to store the maximum score seen so far (initially 0)
    bestScore = 0
    # Create a new variable to store the best word seen so far (initially None)  
    bestWord = None

    # For each word in the wordList
    
    
    for word in wordDict:
        # If you can construct the word from your hand
        if isValidWord(word, hand, wordDict):
            # find out how much making that word is worth
            score = wordDict[word]
            # If the score for that word is higher than your best score
            if (score > bestScore):
                # update your best score, and best word accordingly
                bestScore = score
                bestWord = word
    # return the best word you found.
    return bestWord

def isValidWordInDict(word, hand, wordDict):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    hand[x] = hand.get(x, 0) + 1
    """
    count = 0
    copyHand = hand.copy()
    for i in range(len(word)):
        if word[i] in copyHand:
            if copyHand[word[i]] > 0:
                count += 1
                copyHand[word[i]] = copyHand.get(word[i]) - 1
    if (word in wordDict) and count == len(word):
        return True
    else:
        return False

def getWordDict(wordList,n):
    wordDict= {}

    for word in wordList:
        score = getWordScore(word,n)
        wordDict[word] = score
    return wordDict

#
# Computer plays a hand
#
def compPlayHand(hand, wordList, n, totalScore, wordDict):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    n: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    if (calculateHandlen(hand) > 0) :
        # Display the hand
        
        # computer's word
        word = compChooseWord(hand, wordDict, n)
        
        # If the input is a single period:
        if word == None:
            # End the game (break out of the loop)
            message = ('Total score: ' + str(totalScore) + ' points. Run out of words.')
            score = 0
            return message, hand, totalScore, score, word
            
        # Otherwise (the input is not a single period):
        else :
            # If the word is not valid:
            if (not isValidWordInDict(word, hand, wordDict)) :
                message = ('This is a terrible error! I need to check my own code!')
                score = 0
                word = None
            # Otherwise (the word is valid):
            else :
                # Tell the user how many points the word earned, and the updated total score 
                score = getWordScore(word, n)
                totalScore += score
                message = ('"' + word + '" earned ' + str(score) + ' points. Total: ' + str(totalScore) + ' points')              
                # Update hand and show the updated hand to the user
                hand = updateHand(hand, word)
                
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    message = ('Word: ' + str(word) + " scored " + str(score) + '. Total score: ' +  str(totalScore))
    return message, hand, totalScore, score, word
    
#
# Problem #6: Playing a game
#
#
def playGame(wordDict, wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    """
    usrInp = ""
    usrInp1 = ""
    hand = None
  
    
    while usrInp != 'e':
        usrInp = input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        if usrInp !='r' and usrInp !='n' and usrInp !='e':
            print("Invalid command")
            print()
            continue
        elif usrInp == "r" and hand == None:
            print('You have not played a hand yet. Please play a new hand first!')
            continue    
        elif usrInp == 'e':
            break
        while usrInp1 != 'e':
            usrInp1 = input("Enter u to have yourself play, c to have the computer play: ")
            if usrInp1 !='c' and usrInp1 !='u':
                print("Invalid command")
                print()
                continue
            elif usrInp == 'r' and usrInp1 == 'u' and hand != None:
                playHand(hand, wordList, HAND_SIZE)
                break
            elif usrInp == 'n' and usrInp1 == 'u':
                hand = dealHand(HAND_SIZE)
                playHand(hand, wordList, HAND_SIZE)
                break
            elif usrInp == "r" and usrInp1 == 'c' and hand != None:
                compPlayHand(hand,wordDict,HAND_SIZE)
                break        
            elif usrInp == 'n' and usrInp1 == 'c':
                hand = dealHand(HAND_SIZE)
                compPlayHand(hand,wordDict,HAND_SIZE)
                break

# elif usrInp == "r" and usrInp1 == 'c' and hand == None:
#     print('You have not played a hand yet. Please play a new hand first!')
#     continue




        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    wordDict = getWordDict(wordList, HAND_SIZE)
    playGame(wordDict,wordList)


