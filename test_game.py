import game
import queue
import threading

class MockConsole(object):

    def __init__(self):
        self.stdout = queue.Queue()
        self.stdin = queue.Queue()

    def print(self, string):
        self.stdout.put(string)
        list(map(lambda line: print("<<<", line), string.splitlines()))

    def input(self):
        string = self.stdin.get()
        list(map(lambda line: print(">>>", line), string.splitlines()))
        return string

    def clear(self):
        self.stdout.put(None)

    def get_output(self):
        return self.stdout.get()

    def put_input(self, string=""):
        self.stdin.put(string)


def test_happy_path():
    console = MockConsole()
    runner = game.Game(console)
    game_thread = threading.Thread(target=runner.main, daemon=True)
    game_thread.start()
    console.put_input("Robert")
    for i in range(1, 3):
        console.put_input("travel")
        console.put_input()
        console.put_input("travel")
        console.put_input()
        console.put_input("rest")
        console.put_input()
    console.put_input("quit")
    game_thread.join()


