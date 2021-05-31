#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import random
import json
import sys
import os

try:
    f = open("greWordList.json", 'r')
    global_dict = json.load(f)
    f.close()
except:
    #print("unable to find json file, creating a new one!")
    global_dict = {}

try:
    f = open('vocabulary.json', 'r')
    vocab_dict = json.load(f)
    f.close()
except:
    #print("vocabulary.json does not exist!")
    vocab_dict = {}

def scrapeAListFromVocabulary(url, list_name, length):
    # get the content of the page
    r = requests.get(url)

    # parse the content using html5lib parser
    soup = BeautifulSoup(r.content, 'html5lib')

    temp_content_list = []
    entry = "entry"

    for i in range(length):
        try:
            elem = soup.find("li", {"id":entry+str(i)})
            temp_content_list.append(elem)
        except:
            print("ID: " + entry + str(i) + " Not Found!!")

    temp_word_list = []

    for sup in temp_content_list:
        try:
            word = sup.find("a", "word dynamictext").text
            definition = sup.find("div", "definition").text
        except:
            continue

        try:
            example = sup.find("div", "example").text
        except:
            example = None

        temp_dict = {}
        temp_dict['word'] = word
        temp_dict['definition'] = definition

        if example is not None:
            temp_dict['example'] = example

        temp_word_list.append(temp_dict)

    print(len(temp_word_list))

    if len(temp_word_list) > 0:
        global_dict[list_name] = temp_word_list
        print("list succesfully added!")
        print("updating the local vocabulary....")
        updateVocab()
    else:
        print("UNSUCCESSFUL!!!")

def displayAllLists():
    for list_name in global_dict.keys():
        print("-----------------------------------")
        print("List: ", list_name)
        print("Length: ", len(global_dict[list_name]))
        print("-----------------------------------")
        print()

def scrapeWordMeaning(word):
    print(word)
    url = 'https://www.vocabulary.com/dictionary/' + str(word)
    
    # get the html content using requests
    try:
        r = requests.get(url)
    except:
        return

    # parse the content
    soup = BeautifulSoup(r.content, 'html5lib')

    # create a dict which will be returned
    return_dict = {}

    try:
        return_dict['short_explanation'] = soup.find("p", class_="short").text
    except:
        print("short explanation not found for ", word)
    try:
        return_dict['long_explanation'] = soup.find("p", class_="long").text
    except:
        print("long explanation not found for ", word)
    try:
        return_dict['synonyms'] = soup.find("dd").text
    except:
        print("synonyms not found for ", word)

    return return_dict


def updateVocab():
    for key in global_dict.keys():
        for word_dict in global_dict[key]:
            if word_dict['word'] not in vocab_dict:
                vocab_dict[word_dict['word']] = scrapeWordMeaning(word_dict['word'])
                vocab_dict[word_dict['word']]['definition'] = word_dict['definition']

    with open('vocabulary.json', 'w') as f:
        json.dump(vocab_dict, f)
        print("Local vocabulary successfully updated, current length is ", len(vocab_dict))
        f.close()

def addAList():
    print("\nEnter the url:")
    url = str(input())
    print("Enter the list length")
    length = int(input())
    print("Enter the list name")
    name = str(input())

    scrapeAListFromVocabulary(url, name, length)
    with open('greWordList.json', 'w') as f:
        json.dump(global_dict, f)
        f.close()

def searchInVocab(string = None):
    if string is None:
        word_to_search = str(input())
    else:
        word_to_search = string

    if word_to_search in vocab_dict.keys():
        for key, value in vocab_dict[word_to_search].items():
            print(key + ":\n\n" + value + "\n")
    else:
        print("word not found\n")

def interactiveLearner(list_name = "Miscellaneous", num_words = 20):
    os.system('clear')

    '''
    Explanation of this learner:
    randomly choose num_words from the mentioned list
    First show the complete description of the 
    '''
    print("press enter for the next word or type 'exp' for explanation or enter a word anytime to search in the vocabulary")

    random_word_list = random.sample(global_dict[list_name], num_words)
    
    try:
        f = open('tested_words.json', 'r')
        tested_words = json.load(f)
        f.close()
    except:
        tested_words = {}

    # num words learnt
    count = 0

    for word_dict in random_word_list:
        count += 1
        print("--------------------------------------------------------")
        print("\n" + str(count) + ". " + word_dict['word'] + '  ::  ' + word_dict['definition'])

        # save the word in tested words
        if word_dict['word'] not in tested_words:
            tested_words[word_dict['word']] = word_dict['definition']

        while(True):
            string = str(input())
            if string == 'e' or string == 'exp':
                for key, value in vocab_dict[word_dict['word']].items():
                    print(key + ":\n\n" + value + "\n") 
            elif string == 'q':
                if tested_words.__len__() > 1:
                    f = open('tested_words.json', 'w')
                    json.dump(tested_words, f)
                    f.close()
                return
            elif len(string) <= 1:
                break
            else:
                searchInVocab(string)
        print("-------------------------------------------------------\n")

    if tested_words.__len__() > 1:
        f = open('tested_words.json', 'w')
        json.dump(tested_words, f)
        f.close()

def flashcardleaner(list_name = "Miscellaneous", num_words = 20):
    '''
    Explanation of this flashcardleaner:
    - randomly choose num_words from the mentioned list
    - takes repetation of word in each deck
    - takes randomly sampled one word from num_words
    - first display word and wait for user input 
    
    breaks: when seen all word with all the repetation
    '''

    print('Number of repetition of each word in one deck')
    repetition = int(input())
    os.system('clear')
    print("- press enter for the meaning followed by moving to next word \n- 'mean' or 'm' for meaning without moving to next word \n- type 'exp' for explanation \n- enter a word anytime to search in the vocabulary")
    random_word_list = random.sample(global_dict[list_name], num_words)
    
    try:
        f = open('tested_words_flash.json', 'r')
        tested_words = json.load(f)
        f.close()
    except:
        tested_words = {}

    local_tested_words =[]
    count =0    
    while(count <= num_words*repetition):
        word_dict = random.sample(random_word_list, 1)[0]

        if "count" not in word_dict.keys():
            word_dict['count'] = 1
        while(word_dict['word'] in tested_words and word_dict['count'] >= 3):
            word_dict = random.sample(random_word_list, 1)[0]
        print("--------------------------------------------------------")
        print("\n" + str(count) + ". " + word_dict['word'])
        
        # save the word in tested words
        if word_dict['word'] not in tested_words:
            tested_words[word_dict['word']] = word_dict['definition']
        
        try:
            word_dict['count'] =  word_dict['count'] +1
        except:
            word_dict['count'] =  1

        if word_dict['count'] > 3:
            tested_words[word_dict['word']] = word_dict['definition']
            local_tested_words.append(word_dict['word'])

        mean_printed_already = False
        while(True):     
            string = str(input('Input:'))
            if string == 'm' or string =='meaning' or string =='mean':
                print( 'meaning :: ' + word_dict['definition'])
                mean_printed_already =True 
            elif string == 'e' or string == 'exp':
                for key, value in vocab_dict[word_dict['word']].items():
                    print(key + ":\n\n" + value + "\n") 
            elif string == 'q':
                if tested_words.__len__() > 1:
                    f = open('tested_words_flash.json', 'w')
                    json.dump(tested_words, f)
                    f.close()
                return
            elif len(string) <= 1 or string == "next" or "n":
                if mean_printed_already:
                    break
                print( 'meaning :: ' + word_dict['definition'])
                break
            else:
                    searchInVocab(string)
            if not mean_printed_already:
                print("-------------------------------------------------------\n")
        count =count +1
    if tested_words.__len__() > 1:
        f = open('tested_words_flash.json', 'w')
        json.dump(tested_words, f)
        f.close()

def flashcard():
    lists = list(global_dict.keys())
    print("Which list do you want to use for flash card? Here are the options:\n")
    for i in range(len(lists)):
        print(str(i+1) + ". " + lists[i])
    list_num = int(input())
    
    print("How many words do you want in your flashcard?")
    num_words = int(input())

    flashcardleaner(lists[list_num], num_words)

def Learn():
    lists = list(global_dict.keys())
    #lists.append("Miscellaneous")

    print("Which list do you want to prepare? Here are the options:\n")
    for i in range(len(lists)):
        print(str(i+1) + ". " + lists[i])
    list_num = int(input())
    
    print("How many words do you want to learn today?")
    num_words = int(input())

    interactiveLearner(lists[list_num], num_words)

    return

def meaning_to_word_test():
    # test from the file tested_words.json
    os.system('clear')

    # sample num tuples from the tested word dict
    with open('tested_words.json', 'r') as f:
        word_dict = json.load(f)
        f.close()

    # first find out the words
    words = list(word_dict.keys())

    # now we need to form a dictionay containing meaning: list of words that mean the same
    print("How many words do you want to test from a total of {} words?".format(len(words)))
    num = int(input())

    # sample n random words
    to_test_words = random.sample(words, num)

    # score and count
    score = 0
    count = 0

    # store wrong words
    wrongly_answered = {}

    # form a dictionary of meanings: words
    for word in to_test_words:
        print("-------------------------------------")
        print(word_dict[word])
        print()
        input_word = str(input())

        if input_word == word:
            print('Correct')
            score += 1

        else:
            print('Incorrect, the correct answer is : {}, press `y` to mark it correct'.format(word))
            response = str(input())
            if response.lower() == 'y':
                score += 1
            else:
                wrongly_answered[word] = word_dict[word]

        count += 1

        print("-------------------------------------\n")

        print("-------------------------------------")
        print("Score: {}/{}".format(score, count))
        print("-------------------------------------\n")

    # print the wrong answers
    print("Remember all these\n")

    for word, meaning in wrongly_answered.items():
        print("{} :: {}".format(word, meaning))


def mcq_test():
    # test from the file tested_words.json
    os.system('clear')

    # sample num tuples from the tested word dict
    with open('tested_words.json', 'r') as f:
        word_dict = json.load(f)
        f.close()

    # extract words and meanings in a list
    words = list(word_dict.keys())
    meanings = list(word_dict.values())

    print("How many words do you want to test from a total of {} words?".format(len(words)))
    num = int(input())

    # verify that length of words in more than num
    assert len(words) >= num, "Not enough words to test"

    # sample n random words
    to_test_words = random.sample(words, num)

    # start the tester
    correct = 0
    incorrect = 0
    ans = 0
    ans_ind = 0
    for i in range(num):
        print("------------------------------------------------\n")
        mode = random.randint(0,1)
        if mode == 0:
            print(to_test_words[i] + ": ")

            # sample 4 random meanings
            temp_meanings = random.sample(meanings, 4)
            if word_dict[to_test_words[i]] not in temp_meanings:
                temp_meanings.append(word_dict[to_test_words[i]])
                random.shuffle(temp_meanings)

            # print the meanings
            count = 0
            for meaning in temp_meanings:
                count += 1
                if meaning == word_dict[to_test_words[i]]:
                    ans_ind = count
                print("{}. {}".format(count, meaning))

            # take input the answer
            while True:
                try:
                    ans = int(input())
                    break
                except:
                    continue

        else:
            print(word_dict[to_test_words[i]] + ": \n")

            # sample 4 random words
            temp_words = random.sample(words, 4)
            if to_test_words[i] not in temp_words:
                temp_words.append(to_test_words[i])
                random.shuffle(temp_words)

            # print the words
            count = 0
            for word in temp_words:
                count += 1
                if word == to_test_words[i]:
                    ans_ind = count
                print("{}. {}".format(count, word))

            # take input the answer
            while True:
                try:
                    ans = int(input())
                    break
                except:
                    continue

        # increase the scores
        if ans == ans_ind:
            correct += 1
            print("\nCorrect Answer.")
        else:
            incorrect += 1
            if mode == 0:
                print("The correct answer is : {}\n".format(word_dict[to_test_words[i]]))
            else:
                print("The correct answer is : {}\n".format(to_test_words[i]))

        print("----------------------------------------\n")

        print("+ Score: {} / {}".format(correct, correct + incorrect))
        print()


def vocabLength():
    print(len(vocab_dict))

def printMenu():
    print("------------------------------------")
    print("1. Display all the available lists")
    print("2. Add a list from Vocabulary.com")
    print("3. Learn from a list")
    print("4. Take a test")
    print("5. Update the local Vocabulary")
    print("6. Search a word")
    print("7. Vocab length")
    print("8. FlashCard")
    print("9. Exit")
    print("------------------------------------")


def main():
    print("Welcome to the GRE World!")

    while(True):
        print("Tell us What would you like to do")
        print()

        printMenu()

        choice = int(input())

        if choice == 1:
            displayAllLists()
        elif choice == 2:
            addAList()
        elif choice == 3:
            Learn()
        elif choice == 4:
            print("which test do you want to give?\n1. MCQ\n2. Meaning to Word")
            if int(input()) == 1:
                mcq_test()
            else:
                meaning_to_word_test()
        elif choice == 5:
            updateVocab()
        elif choice == 6:
            searchInVocab()
        elif choice == 7:
            vocabLength()
        elif choice == 8:
            flashcard()
        elif choice == 9:
            sys.exit()

if __name__=='__main__':
    main()

