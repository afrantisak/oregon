#!/usr/bin/env python3


import os
import sys
import game
import random


class Console(object):

    def print(self, string):
        print(string)

    def input(self):
        return input()

    def clear(self):
        os.system('clear')

    def random_integer(self, min, max):
        old_min = 1
        old_max = 100
        old_val = random.randint(old_min, old_max)
        return int(game.re_scale(old_val, old_min, old_max, min, max))


def console_main():
    console = Console()
    runner = game.Game(console)
    main = runner.main()
    return 0


if __name__ == '__main__':
    sys.exit(console_main())
