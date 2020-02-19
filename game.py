#!/usr/bin/env python3

import random
import time
import constants
import ui


# Returns the number of days in the month (28, 30, or 31).
# input: an integer from 1 to 12. 1=January, 2=February, etc.
# output: the number of days in the month. If the input is not in the required range, returns 0.
def days_in_month(days):
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
        self.user = ui.UserInterface(self.console)
        self.miles_traveled = 0
        self.food_remaining = 500
        self.health_level = 5
        self.month = 3
        self.day = 1
        self.sicknesses_suffered_this_month = 0
        self.player_name = None
        self.family_left = 4
        self.dogs_left = 3
        self.eatnum = 9
        self.actions = [
            {'name': 'travel',  'alias': 't', 'handler': self.handle_travel,   'help': 'moves you randomly between 30-60 miles and takes 3-7 days (random).'},
            {'name': 'rest',    'alias': 'r', 'handler': self.handle_rest,     'help': 'increases health 1 level (up to 5 maximum) and takes 2-5 days (random).'},
            {'name': 'hunt',    'alias': 'h', 'handler': self.handle_hunt,     'help': 'adds 20-100 lbs of food and takes 2-5 days (random).'},
            {'name': 'status',  'alias': 's', 'handler': self.handle_status,   'help': 'lists food, health, distance traveled, and day.'},
            {'name': 'help',    'alias': '?', 'handler': self.handle_help,     'help': 'lists all the commands.'},
            {'name': 'quit',    'alias': 'q', 'handler': self.handle_quit,     'help': 'will end the game.'},
        ]

    def miles_remaining(self):
        return constants.MILES_BETWEEN_MISSOURI_AND_OREGON - self.miles_traveled

    def handle_sickness(self):
        self.health_level -= 1
        self.user.print_sick(1, self.health_level)

    def consume_food(self):
        '''allows player to eat 5 punds of food per day'''
        self.food_remaining -= constants.FOOD_EATEN_PER_DAY
        if self.food_remaining < 0:
            self.is_game_over()  # TODO
        else:
            days_food = self.food_remaining / 5
            self.user.print_food_remaining(days_food)

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
    '''gives player a randomly occuring sickness two times each month'''
    # Checks if sickness has happened twice already this month and returns false
    def random_sickness_occurs(self, random_percent):
        chance = 0
        days_left = days_in_month(self.month) - self.day
        if self.sicknesses_suffered_this_month == 0:
            if days_left == 0:
                chance = 100
            else:
                chance = 200 / days_left
        elif self.sicknesses_suffered_this_month == 1:
            if days_left == 0:
                chance = 100
            else:
                chance = 100 / days_left
        if days_left == 0:
            self.sicknesses_suffered_this_month = 0
        if chance >= random_percent:
            self.sicknesses_suffered_this_month += 1
            return True
        else:
            return False

    # Causes a certain number of days to elapse. The days pass one at a time,
    # and each day brings with it a random chance of sickness. The sickness
    # rules are quirky: player is guaranteed to fall ill a certain number of
    # times each month, so illness needs to keep track of month changes.
    # input: an integer number of days that elapse.
    '''Goes to the next day'''
    def advance_game_clock(self, number_days):
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
                self.user.print_month(self.month)

    # enforces the game rules for what happens if a player decides to travel
    '''travels the player 30 - 60 miles in 3 - 7 days'''
    def handle_travel(self):
        self.user.print_wagon()
        miles = random.randint(constants.MIN_MILES_PER_TRAVEL, constants.MAX_MILES_PER_TRAVEL)
        time = random.randint(constants.MIN_DAYS_PER_TRAVEL, constants.MAX_DAYS_PER_TRAVEL)
        self.miles_traveled += miles
        self.user.print_travel(miles, self.miles_remaining())
        self.advance_game_clock(time)

    # enforces the game rules for what happens if a player decides to rest
    def handle_rest(self):
        self.user.print_rest()
        if self.health_level < 5:
          self.health_level = self.health_level + 1
        days_resting = random.randint(constants.MIN_DAYS_PER_REST, constants.MAX_DAYS_PER_REST)
        self.advance_game_clock(days_resting)

    """shortens the code in handle_hunt"""
    def days_to_hunt(self):
        upper_bound = constants.MAX_DAYS_PER_HUNT
        day_at_hunt = random.randint(constants.MIN_DAYS_PER_HUNT, upper_bound)
        self.advance_game_clock(day_at_hunt)

    # the game rules for what happens if a player decides to hunt
    def handle_hunt(self):
        num = random.randint(0,self.eatnum)
        food = self.user.input_hunting_choice()
        if food == "b":
            hunt = random.randint(1, 5)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 120
                self.user.print_killed_animal("Bison", 120)
                self.user.pause()
            else:
                self.user.print_hunt_failed(20)
                self.user.pause()
        elif food == "p":
            hunt = random.randint(1, 3)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 80
                self.user.print_killed_animal("Pig", 80)
                self.user.pause()
            else:
                self.user.print_hunt_failed(33)
                self.user.pause()
        elif food == "s":
            hunt = random.randint(1, 2)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 40
                self.user.print_killed_animal("Snake", 40)
                self.user.pause()
            else:
                self.user.print_hunt_failed(50)
                self.user.pause()
        elif food == "f":
            if self.family_left >= 1:
                self.food_remaining += 80
                self.family_left -= 1
                self.user.print_fratricide(family[num], 80, "All the memories...\nThe screams...")
                ui.family.remove(ui.family[num])
                self.eatnum -= 1
                self.user.pause()
            else:
                self.user.print_all_family_dead()
        elif food == "d":
            if self.dogs_left >= 1:
                self.food_remaining += 60
                self.dogs_left -= 1
                self.user.print_fratricide(dogs[num], 60, "All the memories...\nThe howling...")
                ui.dogs.remove(ui.dogs[num])
                self.eatnum -= 1
                self.user.pause()
            else:
                self.user.print_all_dogs_dead()

    def print_status(self):
        self.user.print_status(self.month, self.day, self.food_remaining, self.health_level, self.miles_traveled, self.dogs_left, self.family_left)

    def handle_status(self):
        self.print_status()

    def handle_help(self):
        self.user.print_help()
        self.user.pause()

    def handle_quit(self):
        self.month = 1
        self.day = 1
        self.is_game_over()

    def handle_invalid_input(self, response):
        self.user.print_invalid_command(response)

    def is_game_over(self):
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

    def is_game_won(self):
        if self.miles_traveled >= constants.MILES_BETWEEN_MISSOURI_AND_OREGON:
            return True
        else:
            return False

    def handle_action(self):
        choices = [{'name': action['name'], 'alias': action['alias']} for action in self.actions]
        aliases = {action['alias']: action['name'] for action in self.actions}
        handlers = {action['name']: action['handler'] for action in self.actions}
        self.user.clear_screen()
        self.print_status()
        self.user.print_action_menu(choices)
        if self.health_level < 3:
            self.user.print_low_health()
        elif self.food_remaining < 100:
            self.user.print_low_food()
        action = self.user.input_action_choice(self.player_name)
        if action in aliases:
            action = aliases[action]
        if action in handlers:
            handlers[action]()
        else:
            self.handle_invalid_input(action)
        return not self.is_game_over()

    def main(self):
        self.user.print_startup_text()
        self.player_name = self.user.input_player_name()
        while self.handle_action():
            self.user.pause()
        if self.is_game_won():
            self.user.print_congratulations()
            randomfamily = random.randint(1, self.eatnum)
            self.user.print_family_left(self.family_left, randomfamily)
            self.user.win()
        else:
            self.user.print_lose()
            self.user.game_over()
