import os
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/visits.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/visits.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/visits.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/visits.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_visits1():
    assert "This is the loop node." == runner1.get_line()
    assert runner1.has_line()
    assert "This is the loop node." == runner1.get_line()
    assert runner1.has_line()
    assert "This is the loop node." == runner1.get_line()
    assert runner1.has_line()
    assert "This is the loop node." == runner1.get_line()
    assert runner1.has_line()
    assert "This is the end." == runner1.get_line()
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.visits['loop'] == 4
    assert runner1.visits['Start'] == 1
    assert runner1.visits['end'] == 1


def test_visits2():
    assert "This is the loop node." == runner2.get_line()
    assert runner2.has_line()
    assert "This is the loop node." == runner2.get_line()
    assert runner2.has_line()
    assert "This is the loop node." == runner2.get_line()
    assert runner2.has_line()
    assert "This is the loop node." == runner2.get_line()
    assert runner2.has_line()
    assert "This is the end." == runner2.get_line()
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.visits['loop'] == 4
    assert runner2.visits['Start'] == 1
    assert runner2.visits['end'] == 1
