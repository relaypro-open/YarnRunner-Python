import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/experimental-newlines.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/experimental-newlines.csv'), 'r')

runner_normal = YarnRunner(compiled_yarn_f, names_csv_f)

# reset file position
compiled_yarn_f.seek(0, 0)
names_csv_f.seek(0, 0)

runner_experimental = YarnRunner(
    compiled_yarn_f, names_csv_f, experimental_newlines=True)


def test_normal_newlines():
    assert "Here's the first line." == runner_normal.get_line()
    assert runner_normal.has_line()
    assert "And the second line." == runner_normal.get_line()
    assert not runner_normal.has_line()
    assert runner_normal.finished


def test_experimental_newlines():
    assert "Here's the first line." == runner_experimental.get_line()
    assert runner_experimental.has_line()
    assert "" == runner_experimental.get_line()
    assert runner_experimental.has_line()
    assert "And the second line." == runner_experimental.get_line()
    assert not runner_experimental.has_line()
    assert runner_experimental.finished
