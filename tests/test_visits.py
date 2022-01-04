import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/visits.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/visits.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f)


def test_visits():
    assert "This is the loop node." == runner.get_line()
    assert runner.has_line()
    assert "This is the loop node." == runner.get_line()
    assert runner.has_line()
    assert "This is the loop node." == runner.get_line()
    assert runner.has_line()
    assert "This is the loop node." == runner.get_line()
    assert runner.has_line()
    assert "This is the end." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished
    assert runner.visits['loop'] == 4
    assert runner.visits['Start'] == 1
    assert runner.visits['end'] == 1
