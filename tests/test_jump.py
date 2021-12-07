import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/jump.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/jump.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f)


def test_start_node_text():
    assert "This is a test of the jump functionality." == runner.get_line()
    assert not runner.has_line()
    assert not runner.finished


def test_start_node_choices():
    choices = runner.get_choices()

    assert len(choices) == 1
    assert choices[0]["choice"] == "begin_jump"
    assert choices[0]["text"] == "Begin Jump"


def test_jumps():
    runner.choose(0)

    assert "Some text is output." == runner.get_line()
    assert runner.has_line()
    assert "The jump is now complete." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished
    assert runner.current_node == 'jump_complete'
