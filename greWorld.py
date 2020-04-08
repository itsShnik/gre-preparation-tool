import requests
from bs4 import BeautifulSoup
import json
import sys

f = open("greWordList.json", 'r')
try:
    global_dict = json.load(f)
except:
    global_dict = {}
f.close()

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

def displayAllLists():
    for list_name in global_dict.keys():
        print("-----------------------------------")
        print("List: ", list_name)
        print("Length: ", len(global_dict[list_name]))
        print("-----------------------------------")
        print()

def printMenu():
    print("------------------------------------------------------------------")
    print("1. Display all the available lists                                ")
    print("2. Add a list from Vocabulary.com                                 ")
    print("3. Learn from a list                                              ")
    print("4. Take a test                                                    ")
    print("5. Exit                                                           ")
    print("------------------------------------------------------------------")

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

def Learn():
    print("function in build")

def test():
    print("function in build")

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
            sys.exit()

if __name__=='__main__':
    main()
