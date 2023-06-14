import os
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/expressions.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/expressions.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/expressions.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/expressions.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1, autostart=False)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2, autostart=False)


def expression_command_handler(first, second, third):
    assert first == "Hello there Sam."
    assert second == "5"
    assert third == "My name is Sam Jose."

def test_expressions1():
    expected_line = "Hello there Sam."

    runner1.resume()

    assert runner1.get_line() == expected_line

def test_expressions2():
    runner2.add_command_handler("test_command", expression_command_handler)
    expected_line = "My name is Sam."

    runner2.resume()
    choices = runner2.get_choices()

    assert runner2.get_line() == expected_line
    assert choices[0]['text'] == "I want to hug Jose"
    assert choices[1]['text'] == "I want to punch Jose"
