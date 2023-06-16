import os
import random
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/functions.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/functions.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/functions.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/functions.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)

# random with seed to ensure deterministic tests
random_seed = random.Random("seed")


def add_numbers(first: int, second: int) -> int:
    return first + second


def dice(faces: int) -> int:
    return random_seed.randrange(1, faces)


def random_range(start: int, stop: int) -> int:
    return random_seed.randrange(start , stop)


runner1.add_command_handler("add_numbers", add_numbers)
runner1.add_command_handler("dice", dice)
runner1.add_command_handler("random_range", random_range)

runner2.add_command_handler("add_numbers", add_numbers)
runner2.add_command_handler("dice", dice)
runner2.add_command_handler("random_range", random_range)


def test_run_functions_1():
    lines = runner1.get_lines()
    assert "One plus one is 2" == lines[0]
    assert "You rolled a six!" == lines[1]
    assert "Gambler: My lucky number is 3!" == lines[2]


def test_run_functions_2():
    lines = runner1.get_lines()
    assert "One plus one is 2" == lines[0]
    assert "You rolled a six!" == lines[1]
    assert "Gambler: My lucky number is 3!" == lines[2]
