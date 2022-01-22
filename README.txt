Hi! This is a mini-project I've been having fun with. If you don't know the game Wordle, its a fun little word game somewhat similar to hangman. It is accessible here: https://www.powerlanguage.co.uk/wordle/ with a nice little archive available here: https://metzger.media/games/wordle-archive/?levels=select


This program is an (non-ideal) solver for Wordle that tells the user what guess to make and then uses the information gained from that guess to come up with a new guess. While I doubt it is perfect, it is consistenty quite good and manages to get most words within 4 guesses with many in 3 and occasionally in 2.

There are a few options to choose from in this file, with 'solver-improved.py' being the most recent. It is more consistent than the original 'solver.py', and almost never fails to obtain an answer, although there are some words that the original is able to guess in 3 that the improved version takes 4 to manage. Finally, there is the oldest 'solver(no-yellow-indices).py' that uses the least information and is thus very quick to enter and is still quite good.

Thanks for reading!
