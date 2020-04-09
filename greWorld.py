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
            if word_dict["word"] not in vocab_dict:
                vocab_dict[word_dict["word"]] = scrapeWordMeaning(word_dict["word"])

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

def searchInVocab():
    while(True):
        word_to_search = str(input())
        if(len(word_to_search) <= 1):
            break
        if word_to_search in vocab_dict.keys():
            print(vocab_dict[word_to_search])
            print()
        else:
            print("word not found\n")

def interactiveLearner(list_name = "Miscellaneous", num_words = 20):
    os.system('clear')

    '''
    Explanation of this learner:
    randomly choose num_words from the mentioned list
    First show the complete description of the 
    '''
    print("press enter for the next word or type 'exp' for explanation")

    random_word_list = random.sample(global_dict[list_name], num_words)

    for word_dict in random_word_list:
        print("\n" + word_dict['word'] + '  ::  ' + word_dict['definition'])
        while(str(input()).startswith('e')):
            for key, value in vocab_dict[word_dict['word']].items():
                print(key + ":\n\n" + value + "\n") 


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

def test():
    print("function in build")

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
    print("8. Exit")
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
            test()
        elif choice == 5:
            updateVocab()
        elif choice == 6:
            searchInVocab()
        elif choice == 7:
            vocabLength()
        elif choice == 8:
            sys.exit()

if __name__=='__main__':
    main()

