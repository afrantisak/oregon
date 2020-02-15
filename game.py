#!/usr/bin/env python3

import random
import time
import ui
import constants


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

    def miles_remaining(self):
        return constants.MILES_BETWEEN_MISSOURI_AND_OREGON - self.miles_traveled

    def handle_sickness(self):
        self.health_level -= 1
        self.user.get_sick(1, self.health_level)

    def consume_food(self):
        '''allows player to eat 5 punds of food per day'''
        self.food_remaining -= constants.FOOD_EATEN_PER_DAY
        if self.food_remaining < 0:
            self.game_is_over()
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
                self.user.print_month(self.month)

    # enforces the game rules for what happens if a player decides to travel
    def handle_travel(self):
        '''travels the player 30 - 60 miles in 3 - 7 days'''
        miles = random.randint(constants.MIN_MILES_PER_TRAVEL, constants.MAX_MILES_PER_TRAVEL)
        time = random.randint(constants.MIN_DAYS_PER_TRAVEL, constants.MAX_DAYS_PER_TRAVEL)
        self.miles_traveled += miles
        self.user.print_travel(miles, self.miles_remaining())
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
        num = random.randint(0,self.eatnum)
        food = self.user.input_hunting_choice()
        if food == "b":
            hunt = random.randint(1, 5)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 120
                self.user.print_killed_animal("Bison", 120)
                ui.user_pause()
                ui.clear()
            else:
                self.user.print_hunt_failed(20)
                ui.user_pause()
                ui.clear()
        elif food == "p":
            hunt = random.randint(1, 3)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 80
                self.user.print_killed_animal("Pig", 80)
                ui.user_pause()
                ui.clear()
            else:
                self.user.print_hunt_failed(33)
                ui.user_pause()
                ui.clear()
        elif food == "s":
            hunt = random.randint(1, 2)
            self.days_to_hunt()
            if hunt == 1:
                self.food_remaining += 40
                self.user.print_killed_animal("Snake", 40)
                ui.user_pause()
                ui.clear()
            else:
                self.user.print_hunt_failed(50)
                ui.user_pause()
                ui.clear()
        elif food == "f":
            if self.family_left >= 1:
                self.food_remaining += 80
                self.family_left -= 1
                self.user.print_fratricide(family[num], 80, "All the memories...\nThe screams...")
                ui.family.remove(ui.family[num])
                self.eatnum -= 1
                ui.user_pause()
                ui.clear()
            else:
                self.user.print_all_family_dead()
        elif food == "d":
            if self.dogs_left >= 1:
                self.food_remaining += 60
                self.dogs_left -= 1
                self.user.print_fratricide(dogs[num], 60, "All the memories...\nThe howling...")
                ui.dogs.remove(ui.dogs[num])
                self.eatnum -= 1
                ui.user_pause()
                ui.clear()
            else:
                self.user.print_all_dogs_dead()

    def handle_status(self):
        self.user.print_status(self.month, self.day, self.food_remaining, self.health_level, self.miles_traveled, self.dogs_left, self.family_left)

    def handle_help(self):
        self.user.print_help()
        ui.user_pause()
        ui.clear()

    def handle_quit(self):
        self.month = 1
        self.day = 1
        self.game_is_over()

    def handle_invalid_input(self, response):
        self.user.print_invalid_command(response)

    def game_is_over(self):
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

    def player_wins(self):
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
        playing = True
        self.user.print_startup_text()
        self.user.pause()
        self.user.clear()
        player_name = self.user.input_player_name()
        self.user.clear()
        self.handle_status()
        while playing:
            self.handle_status()
            self.user.print_action_menu()
            if self.health_level < 3:
                self.user.print_low_health()
            elif self.food_remaining < 100:
                self.user.print_low_food()
            action = self.user.input_action_choice(player_name)
            if action == "travel" or action == "t":
                self.user.travel()
                self.handle_travel()
            elif action == "rest" or action == "r":
                self.user.sleeping()
                self.handle_rest()
            elif action == "hunt" or action == "h":
                self.handle_hunt()
            elif action == "quit" or action == "q":
                self.handle_quit()
            elif action == "help" or action == "?":
                self.handle_help()
            elif action == "status" or action == "s":
                self.handle_status()
                self.user.clear()
            else:
                self.handle_invalid_input(action)
                self.user.pause()
                self.user.clear()
            if self.game_is_over():
                playing = False
        if self.player_wins():
            self.user.print_congratulations()
            self.handle_status()
            randomfamily = random.randint(1, self.eatnum)
            self.user.print_family_left(self.family_left, randomfamily)
            self.user.win()
        else:
            self.user.print_lose()
            self.handle_status()
            self.user.game_over()
