import sys
import game
import json
import queue
import threading


class MockConsole(object):

    def __init__(self):
        self.stdout = queue.Queue()
        self.stdin = queue.Queue()
        self.random = queue.Queue()
        self.timeout = 2

    def print(self, string):
        self.stdout.put(string)
        list(map(lambda line: print_json_to_stderr({"print": line}), string.splitlines()))

    def input(self):
        string = self.stdin.get(timeout=self.timeout)
        list(map(lambda line: print_json_to_stderr({"INPUT": line}), string.splitlines()))
        return string

    def clear(self):
        self.stdout.put(None)

    def get_output(self):
        return self.stdout.get(timeout=self.timeout)

    def put_input(self, string=""):
        self.stdin.put(string)

    def put_random(self, value):
        self.random.put(value)

    def random_integer(self, min, max):
        value = self.random.get(timeout=self.timeout)
        print_json_to_stderr({"RANDM": value})
        assert value >= min and value <= max
        return value


def print_json_to_stderr(line):
    print(json.dumps(line), file=sys.stderr)


def flush_all(queue_object):
    try:
        while True:
            yield queue_object.get_nowait()
    except queue.Empty:
        pass


def test_travel_and_quit():
    console = MockConsole()
    runner = game.Game(console)
    def travel(miles, days, sickness_percentages):
        console.put_random(miles)
        console.put_random(days)
        for sickness_percent in sickness_percentages:
            console.put_random(sickness_percent)
        console.put_input("travel")
        console.put_input()
    game_thread = threading.Thread(target=runner.main, daemon=True)
    game_thread.start()
    console.put_input("Robert")
    for i in range(10):
        travel(miles=50, days=4, sickness_percentages=[10, 20, 30, 40])
    console.put_input("quit")
    game_thread.join()
    assert console.random.empty()
    assert console.stdin.empty()
    assert list(flush_all(console.stdout))[-3:] == [
        '{"Date": "1/1", "Food": 300, "Health": 3, "Miles Traveled": 500, "Dogs Left": 3, "Family Left": 4}',
        "Alas, you lose...",
        "Game Over"]





