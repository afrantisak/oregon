#!/usr/bin/env python3

import os
import time


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


def clear():
  """clears the screen; for the animations and a cleaner look"""
  os.system('clear')


def wagon():
  """the code to print the wagon"""
  clear()
  i = 64
  while i >= 0:
    print("\n\n\n\n")
    print(" "*i , "         /_________\ ")
    print(" "*i , "<}        |       |")
    print(" "*i , " /^^^\----|       |")
    print(" "*i , "[]   []  0}======={0")
    print("______________________________________________________________________")
    i-=8
    time.sleep(0.2)
    clear()


def sleeping():
  """sleeping animation"""
  clear()
  i = 0
  while i < 2:
    print("\n\n\n\n")
    print("                                  /_________\ ")
    print("                         <}        |       |")
    print("                          /^^^\----|       |")
    print("                         []   []  0}======={0")
    print("______________________________________________________________________")
    time.sleep(0.5)
    clear()
    print("\n\n\n")
    print("                                       z")
    print("                                  /_________\ ")
    print("                         <}        |       |")
    print("                          /^^^\----|       |")
    print("                         []   []  0}======={0")
    print("______________________________________________________________________")
    time.sleep(0.5)
    clear()
    print("\n\n")
    print("                                            z  ")
    print("                                       z")
    print("                                  /_________\ ")
    print("                         <}        |       |")
    print("                          /^^^\----|       |")
    print("                         []   []  0}======={0")
    print("______________________________________________________________________")
    time.sleep(0.5)
    clear()
    print("\n")
    print("                                                 z     ")
    print("                                            z       ")
    print("                                       z           ")
    print("                                  /_________\ ")
    print("                         <}        |       |")
    print("                          /^^^\----|       |")
    print("                         []   []  0}======={0")
    print("______________________________________________________________________")
    time.sleep(0.5)
    clear()
    i+=1


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


def you_win():
  print("""\n
        __   __              _    _  _         _
        \ \ / /             | |  | |(_)       | |
         \ V / ___   _   _  | |  | | _  _ __  | |
          \ / / _ \ | | | | | |/\| || || '_ \ | |
          | || (_) || |_| | \  /\  /| || | | ||_|
          \_/ \___/  \__,_|  \/  \/ |_||_| |_|(_)
        """)


def game_over():
  print("""\n
         _____                        _____
        |  __ \                      |  _  |
        | |  \/ __ _ _ __ ___   ___  | | | |_   _____ _ __
        | | __ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__|
        | |_\ \ (_| | | | | | |  __/ \ \_/ /\ V /  __/ |
         \____/\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|
        """)
