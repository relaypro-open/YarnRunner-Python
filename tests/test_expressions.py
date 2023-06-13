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

# TODO: implement a test for expression parsing


def test_expressions1():
    expected_line = "Hello there Sam."

    runner1.resume()

    actual_line = runner1.get_line()
    assert actual_line == expected_line


def test_expressions2():
    expected_line = "Hello there Sam."

    runner2.resume()

    actual_line = runner2.get_line()
    assert actual_line == expected_line
