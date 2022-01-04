import os
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/variables.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/variables.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/variables.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/variables.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_variables1():
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.variables["$value_string"] == "string"
    assert runner1.variables["$value_float"] == 1.25
    assert runner1.variables["$value_bool"] == True
    assert runner1.variables["$value_null"] is None


def test_variables2():
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.variables["$value_string"] == "string"
    assert runner2.variables["$value_float"] == 1.25
    assert runner2.variables["$value_bool"] == True
