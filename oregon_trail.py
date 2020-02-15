#!/usr/bin/env python3


import os
import sys
import game


class Console(object):

    def send(self, string):
        print(string)

    def recv(self):
        return input()

    def clear(self):
        os.system('clear')


def console_main():
    console = Console()
    runner = game.Game(console)
    runner.main()
    return 0


if __name__ == '__main__':
    sys.exit(console_main())
