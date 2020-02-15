#!/usr/bin/env python3

import random
import time
import ui
import constants


# Converts a numeric date into a string.
# inputs: a month in the range 1-12 and a day in the range 1-31
# output: a string like "December 24".
# Note: this function does not enforce calendar rules. It's happy to output impossible strings like "June 95" or "February 31"
def date_as_string(month_number, day_number):
    '''Returns the date as a string'''
    date_string = str(month_number) + "/" + str(day_number)
    return date_string


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


class Game(object):

    def __init__(self, console):
        self.console = console
        self.miles_traveled = 0
        self.food_remaining = 500
        self.health_level = 5
        self.month = 3
        self.day = 1
        self.sicknesses_suffered_this_month = 0
        self.player_name = None
        self.playing = True
        self.family_left = 4
        self.dogs_left = 3
        self.eatnum = 9

    # output: miles remaining until Oregon
    def miles_remaining(self):
        '''Returns the number of miles remaining'''
        remainingmiles = constants.MILES_BETWEEN_MISSOURI_AND_OREGON - self.miles_traveled
        return remainingmiles

    # enforces rules for what happens when a sickness occurs
    def handle_sickness(self):
        '''takes away health from player when sick'''
        self.console.send(self.health_level)
        self.health_level -= 1
        self.console.send("You lost 1 health to sickness!")

    # decreases the food for 1 elapsed day
    def consume_food(self):
        '''allows player to eat 5 punds of food per day'''
        self.food_remaining -= constants.FOOD_EATEN_PER_DAY
        if self.food_remaining < 0:
            self.game_is_over()
        else:
            days_food = self.food_remaining / 5
            self.console.send("You have " + str(days_food) + " days of food left.")


    # Repairs problematic values in the (month, day) model where the day
    # is larger than the number of days in the month. If this happens, advances
    # to the next month and knocks the day value down accordingly. Knows that
    # different months have different numbers of days. Doesn't handle cases where
    # the day is more than 28 days in excess of the limit for that month -- could
    # still end up with an impossible date after this function is called.
    # Returns True if the month/day values were altered, else False.
    def maybe_rollover_month(self):
        '''switches the month to the next when nessacary'''
        if self.month in constants.MONTHS_WITH_31_DAYS:
            if self.day > 31:
                self.month += 1
                if self.month > 12:
                    self.month = 1
                self.day = 1
                return True
            else:
                return False
        elif self.month in constants.MONTHS_WITH_30_DAYS:
            if self.day > 30:
                self.month += 1
                if self.month > 12:
                    self.month = 1
                self.day = 1
                return True
            else:
                return False
        elif self.month in constants.MONTHS_WITH_28_DAYS:
            if self.day > 28:
                self.month += 1
                if self.month > 12:
                    self.month = 1
                self.day = 1
                return True
            else:
                return False
        else:
            return False

    # Calculates whether a sickess occurs on the current day based on how many
    # days remain in the month and how many sick days have already occured this month.
    # If there are N days left in the month, then the chance of a sick day is either
    # 0, 1 out of N, or 2 out of N, depending on whether there have been 2 sick days
    # so far, 1 sick day so far, or no sick days so far. This system guarantees that
    # there will be exactly 2 sick days each month, and incidentally that every day
    # of the month is equally likely to be a sick day
    def random_sickness_occurs(self,  percent):
        '''gives player a randomly occuring sickness two times each month'''
        # Checks if sickness has happened twice already this month and returns false
        if self.sicknesses_suffered_this_month < 2:
            days_left = days_in_month(self.month) - self.day
        if self.sicknesses_suffered_this_month == 0:
            chance = 2 / days_left
        elif self.sicknesses_suffered_this_month == 1:
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
            self.sickness_suffered_this_month = 0
        else:
            return False

    # Causes a certain number of days to elapse. The days pass one at a time,
    # and each day brings with it a random chance of sickness. The sickness
    # rules are quirky: player is guaranteed to fall ill a certain number of
    # times each month, so illness needs to keep track of month changes.
    # input: an integer number of days that elapse.
    def advance_game_clock(self, number_days):
        '''Goes to the next day'''
        stop = number_days + 1
        day_list = range(1, stop)
        for i in day_list:
            self.day += 1
            percent = random.randint(1 , 100)
            sickness = self.random_sickness_occurs(percent)
            if sickness == True:
                self.handle_sickness()
            self.consume_food()
            new_month = self.maybe_rollover_month()
            if new_month == True:
               self.console.send("It is now", ui.NAME_OF_MONTH[self.month] + ".")

    # enforces the game rules for what happens if a player decides to travel
    def handle_travel(self):
        '''travels the player 30 - 60 miles in 3 - 7 days'''
        miles = random.randint(constants.MIN_MILES_PER_TRAVEL, constants.MAX_MILES_PER_TRAVEL)
        time = random.randint(constants.MIN_DAYS_PER_TRAVEL, constants.MAX_DAYS_PER_TRAVEL)
        self.miles_traveled += miles
        miles_remaining = self.miles_remaining()
        self.console.send("You have travelled {miles} miles and have {miles_remaining} miles remaining.".format(**locals()))
        self.advance_game_clock(time)

    # enforces the game rules for what happens if a player decides to rest
    def handle_rest(self):
        ''''carries out the 'rest' command'''
        if self.health_level < 5:
          self.health_level = self.health_level + 1
        days_resting = random.randint(constants.MIN_DAYS_PER_REST, constants.MAX_DAYS_PER_REST)
        self.advance_game_clock(days_resting)

    def days_to_hunt(self):
        """shortens the code in handle_hunt"""
        upper_bound = constants.MAX_DAYS_PER_HUNT
        day_at_hunt = random.randint(constants.MIN_DAYS_PER_HUNT, upper_bound)
        self.advance_game_clock(day_at_hunt)

    # the game rules for what happens if a player decides to hunt
    def handle_hunt(self):
        '''allows players to hunt and gain extra food'''
        num = random.randint(0,self.eatnum)
        food = self.console.recv(ui.hunt_menu).lower()
        ui.clear()
        if food == "b":
            hunt = random.randint(1,5)
            days_to_hunt()
            if hunt == 1:
                self.food_remaining += 120
                self.console.send("You killed a Bison. Food + 120")
                ui.user_pause()
                ui.clear()
            else:
                self.console.send("Hunt Failed 20% Chance")
                ui.user_pause()
                ui.clear()
        elif food == "p":
            hunt = random.randint(1,3)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 80
                self.console.send("You killed a Pig. Food + 80")
                ui.user_pause()
                ui.clear()
            else:
                self.console.send("Hunt Failed 33% Chance")
                ui.user_pause()
                ui.clear()
        elif food == "s":
            hunt = random.randint(1,2)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 40
                self.console.send("You killed a Snake. Food + 40")
                ui.user_pause()
                ui.clear()
            else:
                self.console.send("Hunt Failed 50% Chance")
                ui.user_pause()
                ui.clear()
        elif food == "f":
            if self.family_left >= 1:
                self.food_remaining += 80
                self.family_left -= 1
                self.console.send("You killed and ate" , ui.family[num] , "\nAll the memories... \nThe screams ... \nFood + 80")
                ui.family.remove(ui.family[num])
                self.eatnum -= 1
                ui.user_pause()
                ui.clear()
            else:
                self.console.send("All of your family is dead...")
        elif food == "d":
            if self.dogs_left >= 1:
                self.food_remaining += 60
                self.dogs_left -= 1
                self.console.send("You killed and ate" , ui.dogs[num] , "\nAll the memories... \nFood + 60")
                ui.dogs.remove(ui.dogs[num])
                self.eatnum -= 1
                ui.user_pause()
                ui.clear()
            else:
                self.console.send("All your dogs are dead...")

    # print a player's current status on the journey, including
    # food remaining, health level, distance traveled, and date
    def handle_status(self):
        '''allows players to see what resources they have left'''
        self.console.send("Date: {0}".format(date_as_string(self.month, self.day)))
        self.console.send("Food: {0}".format(self.food_remaining))
        self.console.send("Health: {0}".format(self.health_level))
        self.console.send("Miles Traveled: {0}".format(self.miles_traveled))
        self.console.send("Dogs Left: {0}".format(self.dogs_left))
        self.console.send("Family Left: {0}".format(self.family_left))

    # prints the hep text
    def handle_help(self):
        '''Brings up the help menu'''
        self.console.send(ui.help_menu)
        ui.user_pause()
        ui.clear()

    # enforces what happens when a player decides to quit in the middle of a game
    def handle_quit(self):
        '''allows player to quit the game'''
        self.month = 1
        self.day = 1
        self.game_is_over()

    def handle_invalid_input(self, response):
        """Displays a helpful response if the player inputs an invalid command."""
        self.console.send("'{0}' is not a valid command. Try again.".format(response))

    # returns True if the game is over, otherwise returns False
    def game_is_over(self):
        '''Determines if the game is over'''
        if self.food_remaining < 0:
            return True
        elif self.health_level <= 0:
            return True
        elif self.miles_traveled >= constants.MILES_BETWEEN_MISSOURI_AND_OREGON:
            return True
        elif self.month == 1 and self.day >= 1:
            return True
        else:
            return False

    # returns True if the player wins, otherwise returns False
    def player_wins(self):
        '''Determines if the player has won'''
        if self.miles_traveled >= constants.MILES_BETWEEN_MISSOURI_AND_OREGON:
            return True
        else:
            return False

    def main(self):
        self.miles_traveled = 0
        self.food_remaining = 500
        self.health_level = 5
        self.month = 3
        self.day = 1
        self.sicknesses_suffered_this_month = 0
        player_name = None
        playing = True
        user = ui.UserInterface(self.console)
        self.console.send(ui.welcome_text + ui.help_text + ui.good_luck_text)
        user.pause()
        user.clear()
        player_name = self.console.recv("\nWhat is your name, player? ").title()
        user.clear()
        self.handle_status()
        while playing:
            self.handle_status()
            self.console.send(ui.action_menu)
            if self.health_level < 3:
                self.console.send(ui.low_health_warning)
            elif self.food_remaining < 100:
                self.console.send(ui.low_food_warning)
            self.console.send('\n')
            action = self.console.recv("\nChoose an action, {0} --> ".format(player_name))
            if action == "travel" or action == "t":
                user.wagon()
                self.handle_travel()
            elif action == "rest" or action == "r":
                user.sleeping()
                self.handle_rest()
            elif action == "hunt" or action == "h":
                self.handle_hunt()
            elif action == "quit" or action == "q":
                self.handle_quit()
            elif action == "help" or action == "?":
                self.handle_help()
            elif action == "status" or action == "s":
                self.handle_status()
                user.clear()
            else:
                self.handle_invalid_input(action)
                user.pause()
                user.clear()
            if self.game_is_over():
                playing = False
        if self.player_wins():
            self.console.send("\n\nCongratulations you made it to Oregon alive!\n")
            self.handle_status()
            randomfamily = random.randint(1, self.eatnum)
            if self.family_left == 4:
                self.console.send("Congratulations!, All of your family survived!")
            elif self.family_left == 3:
                self.console.send("Congratulations!, 3 out of 4 of your family members survived!")
            elif self.family_left == 2:
                self.console.send("2 out of 4 of your family members survived. They will never be forgotten.")
            elif self.family_left == 1:
                self.console.send("1 out of 4 of your family members survived. It's just you and", ui.family[randomfamily], "now.")
            elif self.family_left == 0:
                self.console.send("You start your new life alone...")
            user.you_win()
        else:
            self.console.send("\n\nAlas, you lose...\n")
            self.handle_status()
            user.game_over()



