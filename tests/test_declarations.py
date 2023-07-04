import os
from .context import YarnRunner

compiled_yarn = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/declarations.yarnc'), 'rb')
names_csv = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/declarations.csv'), 'r')

runner = YarnRunner(compiled_yarn, names_csv)


def test_variables1():
    # variables are stored
    assert runner.variables["$testBool"] is True
    assert runner.variables["$testNum"] == 1234556
    assert runner.variables["$testString"] == "initial value"

    # the values get to the output without exceptions
    assert runner.get_line() == 'The value of test bool is True'
    assert runner.get_line() == 'The value of test number is 1234556.0'
    assert runner.get_line() == 'The value of test string is "initial value"'

    assert runner.has_line() is False
