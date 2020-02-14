#!/usr/bin/env python3


import sys
import game


class Console(object):

    def send(self, string):
        print(string)

    def recv(self):
        return input()


def console_main():
    console = Console()
    game.main(console)
    return 0


if __name__ == '__main__':
    sys.exit(console_main())
