#!/usr/bin/env python3

import os
import time


help_menu = """
travel: moves you randomly between 30-60 miles and takes 3-7 days (random).
rest: increases health 1 level (up to 5 maximum) and takes 2-5 days (random).
hunt: adds 100 lbs of food and takes 2-5 days (random).
status: lists food, health, distance traveled, and day.
help: lists all the commands.
quit: will end the game.
"""


action_menu = """
"""


hunt_menu = """What would you like to hunt?
    Bison  (b)
    Pig    (p)
    Snake  (s)
    Family (f)
    Dog    (d)
    \n"""


welcome_text = """
Welcome to the Oregon Trail! The year is 1850 and Americans are
headed out West to populate the frontier. Your goal is to travel
by wagon train from Independence, MO to Oregon (2000 miles). You start
on March 1st, and your goal is to reach Oregon by December 31st.
The trail is arduous. Each day costs you food and health. You
can hunt and rest, but you have to get there before winter!
"""


help_text = """
You can take one of 3 actions:

  travel (t) - 
  rest   (r) - 
  hunt   (h) - 

You can also enter one of these commands without using up your turn:

  status (s) - 
  help   (?) - 
  quit   (q) - 
"""


good_luck_text = "\nGood luck, and see you in Oregon!"
low_health_warning = "You are dangerously low on health and could die the next time you travel. Choose option R to heal"
low_food_warning = "You are dangerously low on food and could die the next time you travel. Choose option H to hunt for food"
dogs = ["Ranger" , "Scout" , "Fido" , "Spot" , "Snoopy" , "Charlie" , "Bella" , "Max" , "Woody" , "Daisy"]
family = ["Emma" , "Olivia" , "Ava" , "Isabella" , "Sophia" , "Liam" , "Noah" , "William" , "James" , "Oliver"]
NAME_OF_MONTH = [
    'fake', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]


class UserInterface(object):

    def __init__(self, console):
        self.console = console

    def pause(self):
        self.console.print("Press <Enter> to continue")
        self.console.input()

    def clear_screen(self):
        self.console.clear()

    def print_sick(self, sickness_amount, new_health_level):
        self.console.print("You lost {sickness_amount} health to sickness! Your health is now at {new_health_level}".format(**locals()))

    def print_wagon(self):
        self.console.print("Wagon animation")

    def print_rest(self):
        self.console.print("Sleeping animation")

    def win(self):
        self.console.print("You Win!")

    def game_over(self):
        self.console.print("Game Over")

    def print_food_remaining(self, days_of_food):
        self.console.print("You have " + str(days_of_food) + " days of food left.")

    def print_month(self, month_number):
        self.console.print("It is now" + NAME_OF_MONTH[month_number] + ".")

    def print_travel(self, miles, miles_remaining):
        self.console.print("You have travelled {miles} miles and have {miles_remaining} miles remaining.".format(**locals()))

    def input_hunting_choice(self):
        self.console.print(hunt_menu)
        return self.console.input().lower()

    def print_killed_animal(self, animal, food_delta):
        self.console.print("You killed a {animal}. Food + {food_delta}".format(**locals()))

    def print_fratricide(self, name, food_delta, comments):
        self.console.print("You killed and ate {name}\n{comments}\nFood + {food_delta}".format(**locals()))

    def print_hunt_failed(self, percent):
        self.console.print("Hunt Failed {percent}% Chance".format(**locals()))

    def print_all_family_dead(self):
        self.console.print("All of your family is dead...")

    def print_all_dogs_dead(self):
        self.console.print("All of your dogs are dead...")

    def print_status(self, month, day, food_remaining, health_level, miles_traveled, dogs_left, family_left):
        self.console.print("Date: {0}".format(date_as_string(month, day)))
        self.console.print("Food: {0}".format(food_remaining))
        self.console.print("Health: {0}".format(health_level))
        self.console.print("Miles Traveled: {0}".format(miles_traveled))
        self.console.print("Dogs Left: {0}".format(dogs_left))
        self.console.print("Family Left: {0}".format(family_left))

    def print_help(self):
        self.console.print(help_menu)

    def print_invalid_command(self, command):
        self.console.print("'{command}' is not a valid command. Try again.".format(**locals()))

    def print_startup_text(self):
        self.console.print(welcome_text + help_text + good_luck_text)

    def input_player_name(self):
        self.console.print("\nWhat is your name, player?")
        return self.console.input().title()

    def print_action_menu(self, choices):
        self.console.print("---------------")
        self.console.print("Pick an action:")
        self.console.print("---------------")
        string = ''
        for choice in choices:
            string += "{choice[name]:6} ({choice[alias]:1}) | ".format(**locals())
        self.console.print(string)
        self.console.print("---------------")

    def print_low_health(self):
        self.console.print(low_health_warning)

    def print_low_food(self):
        self.console.print(ui.low_food_warning)

    def input_action_choice(self, player_name):
        self.console.print('Choose an action, {player_name}'.format(**locals()))
        return self.console.input().lower()

    def print_family_left(self, family_left, randomfamily):
        if family_left == 4:
            self.console.print("Congratulations!, All of your family survived!")
        elif family_left == 3:
            self.console.print("Congratulations!, 3 out of 4 of your family members survived!")
        elif family_left == 2:
            self.console.print("2 out of 4 of your family members survived. They will never be forgotten.")
        elif family_left == 1:
            self.console.print("1 out of 4 of your family members survived. It's just you and", ui.family[randomfamily], "now.")
        elif family_left == 0:
            self.console.print("You start your new life alone...")

    def print_congratulations(self):
        self.console.print("\n\nCongratulations you made it to Oregon alive!\n")

    def print_lose(self):
        self.console.print("\n\nAlas, you lose...\n")


# Converts a numeric date into a string.
# inputs: a month in the range 1-12 and a day in the range 1-31
# output: a string like "December 24".
# Note: this function does not enforce calendar rules. It's happy to output impossible strings like "June 95" or "February 31"
def date_as_string(month_number, day_number):
    return str(month_number) + "/" + str(day_number)
