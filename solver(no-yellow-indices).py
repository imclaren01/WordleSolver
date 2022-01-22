import sys


WORD_LIST = []
LETTER_FREQS = {}
GREENS = {}
GUESSES = {}
KNOWN = set()
KNOWN_NOT = set()

with open('wordle-answers-alphabetical.txt') as fi:
    for line in fi:
        WORD_LIST.append((line.replace('\n',''),0))

for word,_ in WORD_LIST:
    for c in set(word):
        if c not in LETTER_FREQS:
            LETTER_FREQS[c] = 1
        else:
            LETTER_FREQS[c] += 1

def score(word: str):
    count = 0
    for c in set(word):
        if c not in KNOWN | KNOWN_NOT:
            count += LETTER_FREQS[c]
    return count

print(f"Iain: {score('orate')}, Mom: {score('abort')}, Brother: {score('angle')}, Keiko: {score('night')}, Adieu: {score('adieu')}, Yaya: {score('their')} ")


def scoreGuess(word):
    count = 0
    for c in set(word):
        if c not in KNOWN:
            count += LETTER_FREQS[c]
        else:
            count+= 2 * LETTER_FREQS[c]
    return count

def hasGreens(word: str):
    for index in GREENS:
        if word[index] != GREENS[index]:
            return False
    return True

def allKnown(word: str):
    word = set(word)
    for letter in KNOWN:
        if letter not in word:
            return False
    return True

def anyKnownNot(word: str):
    for letter in KNOWN_NOT:
        if letter in word:
            return True
    return False

def reorderWords():
    nw = sorted([(x[0],score(x[0])) for x in WORD_LIST], key=lambda x: x[1], reverse= True)
    ng = list(filter(lambda x: not anyKnownNot(x[0]), filter(lambda x: hasGreens(x[0]), filter(lambda x: allKnown(x[0]), WORD_LIST))))

    return nw,ng

def ask():
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT
    KNOWN |= set([item for item in input(f"Now, guess '{WORD_LIST[0][0].upper()}''. Which letters (if any) are now yellow? (seperate letters by spaces): ").split()])
    if input("Was this guess correct? (answer 'y' or 'n'): ") == 'y':
        return True
    gotGreen = input("Were there any greens? (answer 'y' or 'n'): ")
    if gotGreen == 'y':
        greensTemp = [item.split(',') for item in input("Which letters were green? Please enter in format 'c1,n1 c2,n2' where c1 is the first green character and n1 is its location in the word from 1 to 5: " ).split()]
        GREENS.update({int(x[1])-1: x[0] for x in greensTemp})
    KNOWN_NOT |= set(WORD_LIST[0][0]) - (KNOWN | set(GREENS.values()))
    WORD_LIST, GUESSES = reorderWords()
    return False

def guess():
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT
    KNOWN |= set([item for item in input(f"Now, guess '{GUESSES[0][0].upper()}''. Which letters (if any) are now yellow? (seperate letters by spaces): ").split()])
    if input("Was this guess correct? (answer 'y' or 'n'): ") == 'y':
        return True
    gotGreen = input("Were there any greens? (answer 'y' or 'n'): ")
    if gotGreen == 'y':
        greensTemp = [item.split(',') for item in input("Which letters were green? Please enter in format 'c1,n1 c2,n2' where c1 is the first green character and n1 is its location in the word from 1 to 5: " ).split()]
        GREENS.update({int(x[1])-1: x[0] for x in greensTemp})
    KNOWN_NOT |= set(GUESSES[0][0]) - (KNOWN | set(GREENS.values()))
    WORD_LIST, GUESSES = reorderWords()
    return False


def main():
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT
    KNOWN = set([item for item in input("First, guess 'ORATE'. Which letters (if any) are now yellow? (seperate letters by spaces): ").split()])
    if input("Was this guess correct? (answer 'y' or 'n'): ") == 'y':
        print('Nice! Glad to help :). It took only 1 guess to get the answer.')
        sys.exit()
    gotGreen = input("Were there any greens? (answer 'y' or 'n'): ")
    if gotGreen == 'y':
        greensTemp = [item.split(',') for item in input("Which letters were green? Please enter in format 'c1,n1 c2,n2' where c1 is the first green character and n1 is its location in the word from 1 to 5: " ).split()]
        GREENS = {int(x[1])-1: x[0] for x in greensTemp}
    KNOWN_NOT = set('orate') - (KNOWN | set(GREENS.values()))
    WORD_LIST, GUESSES = reorderWords()
    
    tries = 1
    while len(GUESSES) > 20:
        tries += 1
        correct = ask()
        if correct:
            print(f'Nice! Glad to help :). It took {tries} guesses to get the answer.')
            sys.exit()
        print(GUESSES)
    while len(GUESSES) > 1:
        tries += 1
        correct = guess()
        if correct:
            print(f'Nice! Glad to help :). It took {tries} guesses to get the answer.')
            sys.exit()
        print(GUESSES)
    print(f"Based on what you've told me, {GUESSES[0]} should be the correct word. Sorry if it's not!" )
    sys.exit()
        
    

if __name__ == '__main__':
    main()
