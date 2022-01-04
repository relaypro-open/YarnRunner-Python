import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/variables.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/variables.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f)


def test_variables():
    assert not runner.has_line()
    assert runner.finished
    assert runner.variables["$value_string"] == "string"
    assert runner.variables["$value_float"] == 1.25
    assert runner.variables["$value_bool"] == True
    assert runner.variables["$value_null"] is None

# TODO, the variables.yarnc wouldn't compile under YSC 2.0.1-a2eff4c
