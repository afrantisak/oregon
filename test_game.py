import game
import queue


class MockConsole(object):

    def __init__(self):
        self.stdout = queue.Queue()
        self.stdin = queue.Queue()

    def send(self, string):
        self.stdout.put(string)
        print(string)

    def recv(self):
        return self.stdin.get()

    def clear(self):
        self.stdout.put(None)

    def recv_output(self):
        return self.stdout.get()

    def send_input(self, string):
        self.stdin.put(string)


def test_happy_path():
    console = MockConsole()
    runner = game.Game(console)
    console.send_input("")
    console.send_input("Robert")
    console.send_input("t")
    console.send_input("q")
    runner.main()


