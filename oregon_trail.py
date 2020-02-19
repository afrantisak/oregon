#!/usr/bin/env python3


import os
import sys
import game


class Console(object):

    def print(self, string):
        print(string)

    def input(self):
        return input()

    def clear(self):
        os.system('clear')


def console_main():
    console = Console()
    runner = game.Game(console)
    main = runner.main()
    return 0


if __name__ == '__main__':
    sys.exit(console_main())
