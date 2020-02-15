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
---------------
Pick a action:
---------------
Travel (t)
Rest   (r)
Hunt   (h)
---------------
Status (s)
Help   (?)
Quit   (q)

"""


hunt_menu = """What would you like to hunt?
    Bison  (b)
    Pig    (p)
    Snake  (s)
    Family (f)
    Dog    (d)
    \n"""


# welcome text
welcome_text = """
Welcome to the Oregon Trail! The year is 1850 and Americans are
headed out West to populate the frontier. Your goal is to travel
by wagon train from Independence, MO to Oregon (2000 miles). You start
on March 1st, and your goal is to reach Oregon by December 31st.
The trail is arduous. Each day costs you food and health. You
can hunt and rest, but you have to get there before winter!
"""


# help text
help_text = """
You can take one of 3 actions:

  travel (t) - moves you randomly between 30-60 miles and takes 3-7 days (random).
  rest   (r) - increases health 1 level (up to 5 maximum) and takes 2-5 days (random).
  hunt   (h) - adds 20-100 lbs of food and takes 2-5 days (random).

You can also enter one of these commands without using up your turn:

  status (s) - lists food, health, distance traveled, and day.
  help   (?) - lists all the commands.
  quit   (q) - will end the game.
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
        self.console.recv("Press any key to continue")

    def clear(self):
        self.console.clear()

    def wagon(self):
        self.clear()
        i = 64
        while i >= 0:
            self.console.send("\n\n\n\n")
            self.console.send(" "*i + "         /_________\ ")
            self.console.send(" "*i + "<}        |       |")
            self.console.send(" "*i + " /^^^\----|       |")
            self.console.send(" "*i + "[]   []  0}======={0")
            self.console.send("______________________________________________________________________")
            i-=8
            time.sleep(0.2)
            self.clear()

    def sleeping(self):
        self.clear()
        i = 0
        while i < 2:
          self.console.send("\n\n\n\n")
          self.console.send("                                  /_________\ ")
          self.console.send("                         <}        |       |")
          self.console.send("                          /^^^\----|       |")
          self.console.send("                         []   []  0}======={0")
          self.console.send("______________________________________________________________________")
          time.sleep(0.5)
          self.clear()
          self.console.send("\n\n\n")
          self.console.send("                                       z")
          self.console.send("                                  /_________\ ")
          self.console.send("                         <}        |       |")
          self.console.send("                          /^^^\----|       |")
          self.console.send("                         []   []  0}======={0")
          self.console.send("______________________________________________________________________")
          time.sleep(0.5)
          self.clear()
          self.console.send("\n\n")
          self.console.send("                                            z  ")
          self.console.send("                                       z")
          self.console.send("                                  /_________\ ")
          self.console.send("                         <}        |       |")
          self.console.send("                          /^^^\----|       |")
          self.console.send("                         []   []  0}======={0")
          self.console.send("______________________________________________________________________")
          time.sleep(0.5)
          self.clear()
          self.console.send("\n")
          self.console.send("                                                 z     ")
          self.console.send("                                            z       ")
          self.console.send("                                       z           ")
          self.console.send("                                  /_________\ ")
          self.console.send("                         <}        |       |")
          self.console.send("                          /^^^\----|       |")
          self.console.send("                         []   []  0}======={0")
          self.console.send("______________________________________________________________________")
          time.sleep(0.5)
          self.clear()
          i+=1

    def you_win(self):
        self.console.send("""\n
            __   __              _    _  _         _
            \ \ / /             | |  | |(_)       | |
             \ V / ___   _   _  | |  | | _  _ __  | |
              \ / / _ \ | | | | | |/\| || || '_ \ | |
              | || (_) || |_| | \  /\  /| || | | ||_|
              \_/ \___/  \__,_|  \/  \/ |_||_| |_|(_)
            """)

    def game_over(self):
        self.console.send("""\n
             _____                        _____
            |  __ \                      |  _  |
            | |  \/ __ _ _ __ ___   ___  | | | |_   _____ _ __
            | | __ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__|
            | |_\ \ (_| | | | | | |  __/ \ \_/ /\ V /  __/ |
             \____/\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|
            """)
