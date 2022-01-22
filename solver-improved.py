import sys

WORD_LIST = []
GUESSES = []

LETTER_FREQS = {}
GREENS = {}
YELLOWS = {}
KNOWN = set()
KNOWN_NOT = set()

FIRST_WORD = 'orate'

with open('all_words.txt') as fi:
    for line in fi:
        WORD_LIST += [(x,0) for x in map(lambda x: x[1:-2], line.split())]

#Access file of all wordle words
with open('wordle-answers-alphabetical.txt') as fi:
    for line in fi:
        GUESSES.append((line.replace('\n',''),0))

#Create letter frequency map
for word,_ in GUESSES:
    for c in set(word):
        if c not in LETTER_FREQS:
            LETTER_FREQS[c] = 1
        else:
            LETTER_FREQS[c] += 1

def calcFrequencyMap():
    global LETTER_FREQS
    LETTER_FREQS = {}
    for word,_ in GUESSES:
        for c in set(word):
            if c not in LETTER_FREQS:
                LETTER_FREQS[c] = 1
            else:
                LETTER_FREQS[c] += 1

#Score is sum of frequencies of unique letters that we haven't already examined and half frequency of letters we examined but aren't sure where they land yet
def score(word: str):
    count = 0
    for c in set(word):
        if c in LETTER_FREQS:
            if c not in KNOWN | KNOWN_NOT | set(GREENS.values()):
                count += LETTER_FREQS[c]
            elif c in KNOWN and word.index(c) != YELLOWS[c]:
                count += int(LETTER_FREQS[c]/1.5)
    return count


#Score is similar for guesses, except we place preference on letters we have examined but aren't sure where they should be
def scoreGuess(word):
    count = 0
    for c in word:
        print(word, LETTER_FREQS)
        if c in LETTER_FREQS:
            if c not in KNOWN:
                count += LETTER_FREQS[c]
            else:
                count += 3 * LETTER_FREQS[c]
    return count

def hasGreens(word: str):
    for index in GREENS:
        if word[index] != GREENS[index]:
            return False
    return True

def correctYellows(word: str):
    for letter in YELLOWS:
        if word[YELLOWS[letter]] == letter:
            return False
    return True

#Make sure this word contains all letters we know are included in the correct word 
def allKnown(word: str):
    word = set(word)
    for letter in KNOWN:
        if letter not in word:
            return False
    return True

#Make sure this word contains none of the letters we know are NOT included in the correct word
def anyKnownNot(word: str):
    for letter in KNOWN_NOT:
        if letter in word:
            return True
    return False

#Sorts WORD_LIST with new information, filters out guesses list using new information, used by ask() and main()
def reorderWords():
    calcFrequencyMap()
    nw = sorted([(x[0],score(x[0])) for x in WORD_LIST], key=lambda x: x[1], reverse= True)
    ng = [(x[0], scoreGuess(x[0])) for x in sorted(list(filter(lambda x: correctYellows(x[0]),filter(lambda x: not anyKnownNot(x[0]), filter(lambda x: hasGreens(x[0]), filter(lambda x: allKnown(x[0]), GUESSES))))), key= lambda x: scoreGuess(x[0]), reverse=True)]

    return nw,ng


calcFrequencyMap()
newList = [(x[0],score(x[0])) for x in sorted(WORD_LIST, key=lambda x: score(x[0]))]
print(newList[:10])

#Initial stage, tells user what guess to do to obtain the most possible information
#and then updates our global variables
def ask():
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT, YELLOWS
    #locations and characters of yellows
    yellowsTemp = [item.split(',') for item in input(f"Now, guess '{WORD_LIST[0][0].upper()}'. Which letters (if any) are now yellow? Please enter in format 'c1,n1 c2,n2' where c1 is the first yellow character and n1 is its location in the word from 1 to 5: ").split()]
    YELLOWS.update({x[0]: int(x[1])-1 for x in yellowsTemp})
    KNOWN |= set([x[0] for x in yellowsTemp]) 
    if input("Was this guess correct? (answer 'y' or 'n'): ") == 'y':
        return True
    gotGreen = input("Were there any greens? (answer 'y' or 'n'): ")
    if gotGreen == 'y':
        #locations and characters for greens
        greensTemp = [item.split(',') for item in input("Which letters were green? Please enter in format 'c1,n1 c2,n2' where c1 is the first green character and n1 is its location in the word from 1 to 5: " ).split()]
        GREENS.update({int(x[1])-1: x[0] for x in greensTemp})
    KNOWN_NOT |= set(WORD_LIST[0][0]) - (KNOWN | set(GREENS.values()))
    WORD_LIST, GUESSES = reorderWords()
    return False

#Second stage, no longer focusing on obtaining more information, although that still matters
#rather, this section attempts to guess the correct answer, otherwise similar to ask()
def guess():
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT, YELLOWS
    yellowsTemp = [item.split(',') for item in input(f"Now, guess '{GUESSES[0][0].upper()}'. Which letters (if any) are now yellow? Please enter in format 'c1,n1 c2,n2' where c1 is the first yellow character and n1 is its location in the word from 1 to 5: ").split()]
    YELLOWS.update({x[0]: int(x[1])-1 for x in yellowsTemp})
    KNOWN |= set([x[0] for x in yellowsTemp])
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
    global WORD_LIST, GREENS, GUESSES, KNOWN, KNOWN_NOT, YELLOWS
    #This section is essentially the same as ask(), just a few different words for the user
    yellowsTemp = [item.split(',') for item in input(f"First, guess '{FIRST_WORD.upper()}'. Which letters (if any) are now yellow? Please enter in format 'c1,n1 c2,n2' where c1 is the first yellow character and n1 is its location in the word from 1 to 5: ").split()]
    YELLOWS.update({x[0]: int(x[1])-1 for x in yellowsTemp})
    KNOWN = set([x[0] for x in yellowsTemp])
    if input("Was this guess correct? (answer 'y' or 'n'): ") == 'y':
        print('Nice! Glad to help :). It took only 1 guess to get the answer.')
        sys.exit()
    gotGreen = input("Were there any greens? (answer 'y' or 'n'): ")
    if gotGreen == 'y':
        greensTemp = [item.split(',') for item in input("Which letters were green? Please enter in format 'c1,n1 c2,n2' where c1 is the first green character and n1 is its location in the word from 1 to 5: " ).split()]
        GREENS = {int(x[1])-1: x[0] for x in greensTemp}
    KNOWN_NOT = set(FIRST_WORD) - (KNOWN | set(GREENS.values()))
    WORD_LIST, GUESSES = reorderWords()
    
    tries = 1
    while len(GUESSES) > 3:
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
    tries += 1
    print(f"Based on what you've told me, '{GUESSES[0][0].upper()}'' should be the correct word. Sorry if it's not! It took {tries} to guess this answer." )
    sys.exit()
        
    

if __name__ == '__main__':
    main()