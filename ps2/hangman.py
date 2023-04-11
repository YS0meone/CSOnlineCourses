# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"
SEPARATER = "----------"
VOWELS = ['a', 'e', 'i', 'o', 'u']
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



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
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for c in secret_word:
        if c not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    return "".join([c if c in letters_guessed else "_ " for c in secret_word])



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    ret = []
    for c in string.ascii_lowercase:
        if c not in letters_guessed:
            ret.append(c)
    return ret

def get_score(secret_word, chances):
  num_unique = 0
  find = {}
  for c in secret_word:
    if c not in find:
      find[c] = True
      num_unique += 1
  return chances * num_unique

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    chances = 6
    letters_guessed = []
    warnings_left = 3
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secret_word)))
    print("You have {} warnings left.".format(warnings_left))
    print(SEPARATER)
    
    while chances > 0:
      available_letters = get_available_letters(letters_guessed)
      print("You have {} guesses left.".format(chances))
      print("Available letters: {}".format("".join(available_letters)))
      user_guess = input("Please guess a letter: ")

      # Two warning situations
      if not user_guess.isalpha():
        warnings_left -= 1
        if warnings_left == 0:
          chances -= 1
          print("Oops! That is not a valid letter. You lost one chance: {}".format(get_guessed_word(secret_word,letters_guessed)))
          warnings_left = 3
          print(SEPARATER)
          continue
        print("Oops! That is not a valid letter. You have {} warnings left: {}".format(warnings_left, get_guessed_word(secret_word,letters_guessed)))
        print(SEPARATER)
        continue
      if user_guess not in available_letters:
        warnings_left -= 1
        if warnings_left == 0:
          chances -= 1
          print("Oops! You\'ve already guessed that. You lost one chance: {}".format(get_guessed_word(secret_word,letters_guessed)))
          warnings_left = 3
          print(SEPARATER)
          continue
        print("Oops! You\'ve already guessed that. You have {} warnings left: {}".format(warnings_left, get_guessed_word(secret_word,letters_guessed)))
        print(SEPARATER)
        continue

      letters_guessed.append(user_guess.lower())
      if user_guess in secret_word:
          print("Good guess:", get_guessed_word(secret_word, letters_guessed))
          print(SEPARATER)
          if is_word_guessed(secret_word, letters_guessed):
            print("Congratualations, you won!")
            score = get_score(secret_word, chances)
            print("Your total score for this game is:",score)
            break
          continue
      else:
          print("Oops! That letter is not in my word:", get_guessed_word(secret_word,letters_guessed))
          if user_guess in VOWELS:
            chances -= 2
          else:
            chances -= 1
          print(SEPARATER)
    if chances <= 0:
      print("Sorry, you ran out of guesses. The word was else.")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    new_word = "".join(my_word.split())
    if len(new_word) != len(other_word):
      return False
    used = {}
    for c in my_word:
      if c.isalpha() and c not in used:
        used[c] = True
    ptr = 0
    for i in range(len(other_word)):
      if ptr >= len(my_word):
        return False
      if my_word[ptr] == "_":
        if other_word[i] in used:
          return False
        ptr += 2
        continue
      if my_word[ptr] != other_word[i]:
        return False
      ptr += 1
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    ret = []
    find = False
    for word in wordlist:
      if match_with_gaps(my_word, word):
        print(word, end=" ")
        find = True
    if not find:
      print("No matches found")
    else:
      print()

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    chances = 6
    letters_guessed = []
    warnings_left = 3
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secret_word)))
    print("You have {} warnings left.".format(warnings_left))
    print(SEPARATER)
    
    while chances > 0:
      available_letters = get_available_letters(letters_guessed)
      print("You have {} guesses left.".format(chances))
      print("Available letters: {}".format("".join(available_letters)))
      user_guess = input("Please guess a letter: ")
      guessed_word = get_guessed_word(secret_word,letters_guessed)
      # check * first
      if user_guess == "*":
        print("Possible word matches are:")
        show_possible_matches(guessed_word)
        print(SEPARATER)
        continue
      # Two warning situations
      if not user_guess.isalpha():
        warnings_left -= 1
        if warnings_left == 0:
          chances -= 1
          print("Oops! That is not a valid letter. You lost one chance: {}".format(guessed_word))
          warnings_left = 3
          print(SEPARATER)
          continue
        print("Oops! That is not a valid letter. You have {} warnings left: {}".format(warnings_left, guessed_word))
        print(SEPARATER)
        continue
      if user_guess not in available_letters:
        warnings_left -= 1
        if warnings_left == 0:
          chances -= 1
          print("Oops! You\'ve already guessed that. You lost one chance: {}".format(guessed_word))
          warnings_left = 3
          print(SEPARATER)
          continue
        print("Oops! You\'ve already guessed that. You have {} warnings left: {}".format(warnings_left, guessed_word))
        print(SEPARATER)
        continue
      
      # update letters_guessed and guessed_word
      letters_guessed.append(user_guess.lower())
      guessed_word = get_guessed_word(secret_word,letters_guessed)
      if user_guess in secret_word:
          print("Good guess:", guessed_word)
          print(SEPARATER)
          if is_word_guessed(secret_word, letters_guessed):
            print("Congratualations, you won!")
            score = get_score(secret_word, chances)
            print("Your total score for this game is:",score)
            break
          continue
      else:
          print("Oops! That letter is not in my word:", guessed_word)
          if user_guess in VOWELS:
            chances -= 2
          else:
            chances -= 1
          print(SEPARATER)
    if chances <= 0:
      print("Sorry, you ran out of guesses. The word was else.")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)
    # print(is_word_guessed("apple", ['a', 'e', 'b', 'l', 'p']))
    # print(is_word_guessed("apple", ['a', 'e', 'b', 'l']))
    # print(get_available_letters(['a', 'e', 'b', 'l', 'p']))
    # print(get_available_letters(['a', 'e', 'b', 'l']))
    # print(get_guessed_word("apple", ['a', 'e', 'b', 'l', 'p']))
    # print(get_guessed_word("apple", ['a', 'e', 'b', 'l']))
###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    # print(match_with_gaps("te_ t", "tact"))
    # print(match_with_gaps("a_ _ le", "banana"))
    # print(match_with_gaps("a_ _ le", "apple"))
    # print(match_with_gaps("a_ ple", "apple"))
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)