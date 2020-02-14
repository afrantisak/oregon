#!/usr/bin/env python3

import random
import time
import ui
import constants


# beginning values
miles_traveled = 0
food_remaining = 500
health_level = 5
month = 3
day = 1
sicknesses_suffered_this_month = 0
player_name = None
playing = True
family_left = 4
dogs_left = 3
eatnum = 9


# Converts a numeric date into a string.
# inputs: a month in the range 1-12 and a day in the range 1-31
# output: a string like "December 24".
# Note: this function does not enforce calendar rules. It's happy to output impossible strings like "June 95" or "February 31"
def date_as_string(month_number, day_number):
    '''Returns the date as a string'''
    date_string = str(month_number) + "/" + str(day_number)
    return date_string


# output: miles remaining until Oregon
def miles_remaining():
    '''Returns the number of miles remaining'''
    remainingmiles = constants.MILES_BETWEEN_MISSOURI_AND_OREGON - miles_traveled
    return remainingmiles


# Returns the number of days in the month (28, 30, or 31).
# input: an integer from 1 to 12. 1=January, 2=February, etc.
# output: the number of days in the month. If the input is not in the required range, returns 0.
def days_in_month(days):
    '''returns how many days are in each month'''
    if days < 1 or days > 12:
        return 0
    else:
        if days in constants.MONTHS_WITH_31_DAYS:
            return 31
        elif days in constants.MONTHS_WITH_30_DAYS:
            return 30
        else:
            return 28


# Calculates whether a sickess occurs on the current day based on how many
# days remain in the month and how many sick days have already occured this month.
# If there are N days left in the month, then the chance of a sick day is either
# 0, 1 out of N, or 2 out of N, depending on whether there have been 2 sick days
# so far, 1 sick day so far, or no sick days so far. This system guarantees that
# there will be exactly 2 sick days each month, and incidentally that every day
# of the month is equally likely to be a sick day
def random_sickness_occurs(sicknesses_suffered_this_month, day, percent):
    '''gives player a randomly occuring sickness two times each month'''
    # Checks if sickness has happened twice already this month and returns false
    if sicknesses_suffered_this_month < 2:
        days_left = days_in_month(month) - day
    if sicknesses_suffered_this_month == 0:
        chance = 2 / days_left
    elif sicknesses_suffered_this_month == 1:
        chance = 1 / days_left
    chance = float(chance)
    chance = format(chance, '.2f')
    chance = float(chance)
    chance *= 100
    chance = round(chance)
    if chance >= percent:
        return True
    else:
        return False
    if days_left == 0:
        sickness_suffered_this_month = 0
    else:
        return False


# enforces rules for what happens when a sickness occurs
def handle_sickness():
    '''takes away health from player when sick'''
    global health_level
    print(health_level)
    health_level -= 1
    print("You lost 1 health to sickness!")


# decreases the food for 1 elapsed day
def consume_food():
    '''allows player to eat 5 punds of food per day'''
    global food_remaining
    food_remaining -= constants.FOOD_EATEN_PER_DAY
    if food_remaining < 0:
        game_is_over()
    else:
        days_food = food_remaining / 5
        print("You have " + str(days_food) + " days of food left.")


# Repairs problematic values in the global (month, day) model where the day
# is larger than the number of days in the month. If this happens, advances
# to the next month and knocks the day value down accordingly. Knows that
# different months have different numbers of days. Doesn't handle cases where
# the day is more than 28 days in excess of the limit for that month -- could
# still end up with an impossible date after this function is called.
# Returns True if the global month/day values were altered, else False.
def maybe_rollover_month():
    '''switches the month to the next when nessacary'''
    global month
    global day
    if month in constants.MONTHS_WITH_31_DAYS:
        if day > 31:
            month += 1
            if month > 12:
                month = 1
            day = 1
            return True
        else:
            return False
    elif month in constants.MONTHS_WITH_30_DAYS:
        if day > 30:
            month += 1
            if month > 12:
                month = 1
            day = 1
            return True
        else:
            return False
    elif month in constants.MONTHS_WITH_28_DAYS:
        if day > 28:
            month += 1
            if month > 12:
                month = 1
            day = 1
            return True
        else:
            return False
    else:
        return False


# Causes a certain number of days to elapse. The days pass one at a time,
# and each day brings with it a random chance of sickness. The sickness
# rules are quirky: player is guaranteed to fall ill a certain number of
# times each month, so illness needs to keep track of month changes.
# input: an integer number of days that elapse.
def advance_game_clock(number_days):
    '''Goes to the next day'''
    global sicknesses_suffered_this_month
    global day
    stop = number_days + 1
    day_list = range(1, stop)
    global day
    for i in day_list:
        day += 1
        percent = random.randint(1 , 100)
        sickness = random_sickness_occurs(sicknesses_suffered_this_month , day , percent)
        if sickness == True:
            handle_sickness()
        consume_food()
        new_month = maybe_rollover_month()
        if new_month == True:
           print("It is now", ui.NAME_OF_MONTH[month] + ".")


# enforces the game rules for what happens if a player decides to travel
def handle_travel():
    '''travels the player 30 - 60 miles in 3 - 7 days'''
    miles = random.randint(constants.MIN_MILES_PER_TRAVEL, constants.MAX_MILES_PER_TRAVEL)
    time = random.randint(constants.MIN_DAYS_PER_TRAVEL, constants.MAX_DAYS_PER_TRAVEL)
    global miles_traveled
    miles_traveled += miles
    print("You have travelled", miles, "miles and have", miles_remaining(), "miles remaining.")
    advance_game_clock(time)


# enforces the game rules for what happens if a player decides to rest
def handle_rest():
    ''''carries out the 'rest' command'''
    global health_level
    if health_level < 5:
      health_level = health_level + 1
    days_resting = random.randint(constants.MIN_DAYS_PER_REST, constants.MAX_DAYS_PER_REST)
    advance_game_clock(days_resting)


def days_to_hunt():
    """shortens the code in handle_hunt"""
    upper_bound = constants.MAX_DAYS_PER_HUNT
    day_at_hunt = random.randint(constants.MIN_DAYS_PER_HUNT, upper_bound)
    advance_game_clock(day_at_hunt)


# the game rules for what happens if a player decides to hunt
def handle_hunt():
    '''allows players to hunt and gain extra food'''
    global eatnum
    num = random.randint(0,eatnum)
    food = input(ui.hunt_menu).lower()
    ui.clear()
    global food_remaining
    global dogs_left
    global family_left
    if food == "b":
        hunt = random.randint(1,5)
        days_to_hunt()
        if hunt == 1:
            food_remaining += 120
            print("You killed a Bison. Food + 120")
            ui.user_pause()
            ui.clear()
        else:
            print("Hunt Failed 20% Chance")
            ui.user_pause()
            ui.clear()
    elif food == "p":
        hunt = random.randint(1,3)
        days_to_hunt()
        if hunt == 1:
            food_remaining += 80
            print("You killed a Pig. Food + 80")
            ui.user_pause()
            ui.clear()
        else:
            print("Hunt Failed 33% Chance")
            ui.user_pause()
            ui.clear()
    elif food == "s":
        hunt = random.randint(1,2)
        days_to_hunt()
        if hunt == 1:
            food_remaining += 40
            print("You killed a Snake. Food + 40")
            ui.user_pause()
            ui.clear()
        else:
            print("Hunt Failed 50% Chance")
            ui.user_pause()
            ui.clear()
    elif food == "f":
        if family_left >= 1:
            food_remaining += 80
            family_left -= 1
            print("You killed and ate" , ui.family[num] , "\nAll the memories... \nThe screams ... \nFood + 80")
            ui.family.remove(ui.family[num])
            eatnum -= 1
            ui.user_pause()
            ui.clear()
        else:
            print("All of your family is dead...")
    elif food == "d":
        if dogs_left >= 1:
            food_remaining += 60
            dogs_left -= 1
            print("You killed and ate" , ui.dogs[num] , "\nAll the memories... \nFood + 60")
            ui.dogs.remove(ui.dogs[num])
            eatnum -= 1
            ui.user_pause()
            ui.clear()
        else:
            print("All your dogs are dead...")


# print a player's current status on the journey, including
# food remaining, health level, distance traveled, and date
def handle_status():
    '''allows players to see what resources they have left'''
    print("Date:", date_as_string(month, day))
    print("Food:", food_remaining)
    print("Health:", health_level)
    print("Miles Traveled:", miles_traveled)
    print("Dogs Left:", dogs_left)
    print("Family Left:", family_left)


# prints the hep text
def handle_help():
    '''Brings up the help menu'''
    print(ui.help_menu)
    ui.user_pause()
    ui.clear()


# enforces what happens when a player decides to quit in the middle of a game
def handle_quit():
    '''allows player to quit the game'''
    global month
    global day
    month = 1
    day = 1
    game_is_over()


def handle_invalid_input(response):
    """Displays a helpful response if the player inputs an invalid command."""
    print("'{0}' is not a valid command. Try again.".format(response))


# returns True if the game is over, otherwise returns False
def game_is_over():
    '''Determines if the game is over'''
    if food_remaining < 0:
        return True
    elif health_level <= 0:
        return True
    elif miles_traveled >= constants.MILES_BETWEEN_MISSOURI_AND_OREGON:
        return True
    elif month == 1 and day >= 1:
        return True
    else:
        return False


# returns True if the player wins, otherwise returns False
def player_wins():
    '''Determines if the player has won'''
    if miles_traveled >= constants.MILES_BETWEEN_MISSOURI_AND_OREGON:
        return True
    else:
        return False


def main(console):
    # --------------------------------------------------------------------------------
    # Game State -- global variables that collectively represent the state of the game
    # --------------------------------------------------------------------------------
    miles_traveled = 0
    food_remaining = 500
    health_level = 5
    month = 3
    day = 1
    sicknesses_suffered_this_month = 0
    player_name = None
    playing = True
    print(ui.welcome_text + ui.help_text + ui.good_luck_text)
    ui.user_pause()
    ui.clear()
    player_name = input("\nWhat is your name, player? ").title()
    ui.clear()
    handle_status()
    while playing:
        handle_status()
        print(ui.action_menu)
        if health_level < 3:
            print(ui.low_health_warning)
        elif food_remaining < 100:
            print(ui.low_food_warning)
        print()
        action = input("\nChoose an action, {0} --> ".format(player_name))
        if action == "travel" or action == "t":
            ui.wagon()
            handle_travel()
        elif action == "rest" or action == "r":
            ui.sleeping()
            handle_rest()
        elif action == "hunt" or action == "h":
            handle_hunt()
        elif action == "quit" or action == "q":
            handle_quit()
        elif action == "help" or action == "?":
            handle_help()
        elif action == "status" or action == "s":
            handle_status()
            ui.clear()
        else:
            handle_invalid_input(action)
            ui.user_pause()
            ui.clear()
        if game_is_over():
            playing = False
    if player_wins():
        print("\n\nCongratulations you made it to Oregon alive!\n")
        handle_status()
        randomfamily = random.randint(1, eatnum)
        if family_left == 4:
            print("Congratulations!, All of your family survived!")
        elif family_left == 3:
            print("Congratulations!, 3 out of 4 of your family members survived!")
        elif family_left == 2:
            print("2 out of 4 of your family members survived. They will never be forgotten.")
        elif family_left == 1:
            print("1 out of 4 of your family members survived. It's just you and", ui.family[randomfamily], "now.")
        elif family_left == 0:
            print("You start your new life alone...")
        ui.you_win()
    else:
        print("\n\nAlas, you lose...\n")
        handle_status()
        ui.game_over()



