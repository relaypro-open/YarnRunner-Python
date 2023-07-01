import os
from .context import YarnRunner

compiled_yarn = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/stdlib.yarnc'), 'rb')
names_csv = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/stdlib.csv'), 'r')

runner = YarnRunner(compiled_yarn, names_csv, autostart=False)


def test_variables2():
    runner.resume()

    # we are just happy nothing exploded while running
    # that means every stdlib function is invoked correctly
    # if this wasn't the case, we would have an exception
    assert runner.finished
