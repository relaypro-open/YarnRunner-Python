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

# autostart=False so the runner doesn't start before the functions are registered
runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1, autostart=False)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2, autostart=False)


def add_numbers(first: int, second: int) -> int:
    return int(first + second)


def dice(faces: int) -> int:
    return int(6)


def random_range(start: int, stop: int) -> int:
    return int(6)


def test_run_functions_1():
    runner1.add_function_handler("add_numbers", add_numbers)
    runner1.add_function_handler("dice", dice)
    runner1.add_function_handler("random_range", random_range)

    runner1.resume()

    lines = runner1.get_lines()
    assert lines[0] == "One plus one is 2"
    assert lines[1] == "You rolled a six!"
    assert lines[2] == "Gambler: My lucky number is 6!"


def test_run_functions_2():
    runner2.add_function_handler("add_numbers", add_numbers)
    runner2.add_function_handler("dice", dice)
    runner2.add_function_handler("random_range", random_range)

    runner2.resume()

    lines = runner2.get_lines()
    assert lines[0] == "One plus one is 2"
    assert lines[1] == "You rolled a six!"
    assert lines[2] == "Gambler: My lucky number is 6!"


def test_function_invocation_without_handler():
    function_name = "add_numbers"

    runner3 = YarnRunner(compiled_yarn_f2, names_csv_f2, autostart=False)
    try:
        runner3.resume()

        # the runner should throw an error
        raise Exception(
            "The runner ran without any issues. This test should fail. An Exception was expected.")
    except Exception as e:
        assert str(
            e) == f"The function `{function_name}` is not implemented, and is not registered as a custom function."
