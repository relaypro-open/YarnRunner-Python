import os
from .context import YarnRunner

compiled_yarn = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/standart-lib.yarnc'), 'rb')
names_csv = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/standart-lib.csv'), 'r')

runner = YarnRunner(compiled_yarn, names_csv, autostart=False)


def test_variables2():
    runner.resume()
    assert runner.finished
