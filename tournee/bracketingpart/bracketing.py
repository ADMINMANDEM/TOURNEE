import math
import ast
import time
import sys


def delay_print(string):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


# Merge two sorted lists
def join(list1, list2, key):
    list3 = []
    while len(list1) > 0 and len(list2) > 0:
        if key(list1[0]) < key(list2[0]):
            list3.append(list1[0])
            list1.pop(0)
        else:
            list3.append(list2[0])
            list2.pop(0)

    list3 = list3 + list1 + list2
    return list3


# Recursively merge sort the input list
# 1) Split it in half
# 2) Merge sort each half (recursively)
# 3) Join the two sorted halves (using join)
def merge_sort(list3, key):
    if len(list3) <= 1:
        return list3

    half = len(list3) // 2
    list1 = list3[:half]

    list1 = merge_sort(list1, key)
    list2 = merge_sort(list3[half:], key)
    return join(list1, list2, key)


def generate(teams_in_tournament):
    sorted_teams = merge_sort(teams_in_tournament, key=lambda team: team[1])
    # Pre-round to ensure next round is power of 2
    round_teams = [team[0] for team in sorted_teams]
    matches = bracket(round_teams)

    return matches


def bracket(teams):
    length = len(teams)
    return [(teams[i], teams[length - i - 1]) for i in range(int(length / 2))]


inputted_list = input('''
    '._==_==_=_.'    _____   _____   _   _  ______   _   _   _____   _____
    .-\:      /-.   |_   _| |  _  | | | | | | ___ \ | \ | | |  ___| |  ___
   | (|:.     |) |    | |   | | | | | | | | | |_/ / |  \| | | |__   | |__  
    '-|:.     |-'     | |   | | | | | | | | |    /  | . ` | |  __|  |  __| 
      \::.    /       | |   \ \_/ / | |_| | | |\ \  | |\  | | |___  | |___ 
       '::. .'        \_/    \___/   \___/  \_| \_| \_| \_/ \____/  \____/ 
         ) (
       _.' '._
      `"""""""`
Hello! Welcome to the bracketing part of TOURNEE!

You should have received some code from the main website, it should look like this: 

[ ('Team1', 1), ('Team2', 2) ]

Highlight it with your mouse and then press CTRL + C OR right-click it and press "Copy"

Come back here and Paste it below (you can do this by using CTRL + SHIFT + V or right-clicking and pressing on "Paste as plain text")

Paste list of teams here and press enter:

''')

passed = False
while not passed:
    try:
        inputted_list = ast.literal_eval(str(inputted_list))
        generate(inputted_list)
    except (ValueError, SyntaxError, TypeError, KeyboardInterrupt):
        passed = False
    else:
        inputted_list = ast.literal_eval(str(inputted_list))
        if len(inputted_list) >= 2:
            passed = True
            break
        else:
            passed = False
            print("You must have 2 teams or more for a tournament")
    inputted_list = input("Please use the provided code with the format: [ ('Team1', 1), ('Team2', 2) ]\n")


print("\n" * 100)

round_number = 1
positions = []

while len(inputted_list) > 1:
    fixtures = generate(inputted_list)
    team1s = [x[0] for x in fixtures]
    team2s = [x[1] for x in fixtures]
    if len(inputted_list) == 2:
        print("It's the FINAL")
    else:
        print("The matches for ROUND " + str(round_number) + " are:\n")
    round_number += 1
    for i in range(0, len(fixtures)):
        time.sleep(0.5)
        delay_print("Game " + str(i + 1) + ": " + str(team1s[i] + " vs " + str(team2s[i])) + "\n")
        time.sleep(1)
    for i in range(0, len(fixtures)):
        team1 = fixtures[i][0]
        team2 = fixtures[i][1]
        this = True
        while this:
            time.sleep(0.5)
            print("-----------------------------------------------------------------\n" + "Game " + str(
                i + 1) + ": " + str(team1) + " vs " + team2)
            time.sleep(0.5)
            winner = input("Which team won? \nUse '1' for " + str(team1) + " and '2' for " + str(team2) + " and then press 'Enter'\n")
            if winner == "1":
                for element in inputted_list:
                    if element[0] == team2:
                        inputted_list.remove(element)
                        positions.insert(0, element)
                this = False
            elif winner == "2":
                for element in inputted_list:
                    if element[0] == team1:
                        inputted_list.remove(element)
                        positions.insert(0, element)
                this = False
            else:
                print("Please just enter '1' or '2'")
                this = True

print("The winner is " + str(inputted_list[0][0]))


def ordinal(number):
    number = int(number)
    ord_bit = ['th', 'st', 'nd', 'rd', 'th'][min(number % 10, 4)]
    if 11 <= (number % 100) <= 13:
        ord_bit = 'th'
    return str(number) + ord_bit


for i in range(0, len(positions)):
    print("In " + ordinal(str(i + 2)) + " place was: " + str(positions[i][0]))
