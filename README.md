# gre-preparation-tool

A tool to prepare for GRE using command line terminal. Build in process.

## Provided Vocabulary lists

1. Manhattan GRE Complete
2. GRE Complete vocabulary list
3. Barren 333
4. 900+ essential gre words

## Features

1. **Vocabulary Addition** Add vocabulary lists from [vocabulary.com](vocabulary.com)

	- You can add as many vocab lists as you want, just put in the link and the scraper module will scrape the list and save it.
	- Currently, 4 lists are addes. Details in Provided vocabulary list section

2. **Learn from list**: Learn words from any of the provided list

	- An interactive learner to memorize the word meanings
	- Store learned vocabulary in tested_words.json

3. **Tests**: Take tests to memorize the word meanings

	- Supports two different types of tests 
		1. MCQ 
		2. Meaning to words

4. **Word Search**: Search for any word in the vocabulary 

	- The vocabulary consists of all the words in all the lists.

5. **Learn with Flashcards**: simple flash cards with reviewing words.
	- The word with repetation display randomly. Number of repetation is set by users. 
	- Store learned vocabulary in tested_words_flash.json

## Run

Just follow the instruction after running ```./greworld.py```

```
./greWorld.py

Welcome to the GRE World!
Tell us What would you like to do

------------------------------------
1. Display all the available lists
2. Add a list from Vocabulary.com
3. Learn from a list
4. Take a test
5. Update the local Vocabulary
6. Search a word
7. Vocab length
8. FlashCard
9. Exit
------------------------------------
3 #user input
Which list do you want to prepare? Here are the options:

1. Manhattan GRE Complete
2. GRE Complete vocabulary list
3. Barren 333
4. 900+ essential gre words

How many words do you want to learn today?
20 #user input
```
you are ready to learn in clear prompt

```
press enter for the next word or type 'exp' for explanation or enter a word anytime to search in the vocabulary
--------------------------------------------------------

1. inured  ::  made tough by habitual exposure
exp

short_explanation:

If you have gotten so many mosquito bites in your life that they no longer bother you, you have become inured to them. This means you have become accustomed to tolerating them.

long_explanation:

This adjective is derived from the 16th-century phrase in ure, meaning “in use” or “in practice.” When you are inured to something, you have probably had a lot of persistent exposure to it, and it’s usually something negative. People can become inured to pain, inured to violence, and even inured to the sound of a little yappy dog that won’t stop barking.

synonyms:

enured, hardened

definition:

made tough by habitual exposure

q #user input to quit program
# It will saved learn vocabulary in json file 
```

## Miscellanous
- You may contact us by opening an issue on this repo. Please allow 2-3 days of time to address the issue.
- **LICENSE**: MIT
