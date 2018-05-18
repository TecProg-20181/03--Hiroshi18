import random
import logging
import string

WORDLIST_FILENAME = "words.txt"
GUESSES_MAX = 8
logging.basicConfig(filename='hangman.log', level=logging.DEBUG)


class Word:

    def __init__(self):
        self.word = ''
        self.lettersGuessed = []

    def file_check(self, file_name):
        try:
            return open(file_name, "r")
        except IOError:
            print "Error: File does not exist."
            logging.critical("File does not exist")
            logging.critical(IOError)
            exit()

    def load_words(self):
        print "Loading word list from file..."
        logging.info("Loading word list from file...")

        # inFile: file
        self.inFile = self.file_check(WORDLIST_FILENAME)

        logging.debug('File Exists!')

        # line: string
        line = self.inFile.readline()

        # wordlist: list of strings
        wordlist = string.split(line)

        logging.debug('Word list created')

        logging.info("%d words loaded.", len(wordlist))

        self.word = random.choice(wordlist).lower()
        logging.debug("The Secret Word is %s ", self.word)

    def is_word_guessed(self):
        for letter in self.word:
            if letter in self.lettersGuessed:
                pass
            else:
                return False
        return True

    def get_guessed_word(self):
        guessed = ''
        for letter in self.word:
            if letter in self.lettersGuessed:
                guessed = guessed + letter
            else:
                guessed = guessed + '_ '
        return guessed

    def get_available_letters(self):
        available = string.ascii_lowercase
        for letter in available:
            if letter in self.lettersGuessed:
                available = available.replace(letter, '')
        return available
    
    def different_letters(self):
        return len(set(self.word))


class Hangman:
    def __init__(self):
        self.guesses = GUESSES_MAX
        self.secretWord = Word()
        self.secretWord.load_words()

    def welcome_message(self):
        print 'Welcome to the game, Hangam!'
        print 'I am thinking of a word that is', len(self.secretWord.word), ' letters long.'
        print 'Has', self.secretWord.different_letters(), 'different letters'
        print '-------------'
    
    def word_test(self):
        while self.secretWord.different_letters() > self.guesses:
            print 'We have different letters is greater than the number of attempts\nNew Word?\ny- yes\nn- any other'
            input = raw_input()
            if input == 'y':
                self.secretWord.load_words()
            else:
                break

    def game_start(self):
        while self.secretWord.is_word_guessed() == False and self.guesses > 0:
            print 'You have ', self.guesses, 'self.guesses left.'
            available = self.secretWord.get_available_letters()
            print 'Available letters', available
            letter = raw_input('Please guess a letter or the word: ')

            while letter.isalpha() is False or (len(letter) != 1 and len(letter) != len(self.secretWord.word)):
                letter = raw_input('The input must a single letter or the word:')
                logging.debug("Entered validation because, not letter %s, tried word %s, word wrong size %s", letter.isalpha(),
                              (len(letter) == 1 ), len(letter) == len(self.secretWord.word))

            if letter in self.secretWord.lettersGuessed:
                guessed = self.secretWord.get_guessed_word()
                print 'Oops! You have already guessed that letter: ', guessed
                logging.info("Already guessed that letter")

            elif letter == self.secretWord.word:
                print 'Congratulations, you won!'
                logging.info("Won Guessed the Word")
                break

            elif letter in self.secretWord.word:
                self.secretWord.lettersGuessed.append(letter)
                guessed = self.secretWord.get_guessed_word()
                print 'Good Guess: ', guessed
                logging.info("Guessed good letter")

            else:
                self.guesses -= 1
                self.secretWord.lettersGuessed.append(letter)
                guessed = self.secretWord.get_guessed_word()
                print 'Oops! That letter is not in my word: ', guessed
                logging.info("Guessed wrong letter")

            print '------------'
        else:
            if self.secretWord.is_word_guessed():
                print 'Congratulations, you won!'
                logging.info("Won")
            else:
                print 'Sorry, you ran out of guesses. The word was ', self.secretWord.word, '.'
                logging.info("Lose")

    def main(self):
        self.welcome_message()
        self.word_test()
        self.game_start()


if __name__ == '__main__':
    game = Hangman()
    game.main()
