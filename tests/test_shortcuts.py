import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/shortcuts.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/shortcuts.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f)


def test_start_node_text():
    assert "This is a test of shortcut functionality." == runner.get_line()
    assert not runner.has_line()
    assert not runner.finished


def test_start_node_choices():
    choices = runner.get_choices()

    assert len(choices) == 4
    assert choices[0]["text"] == "Option 1"
    assert choices[1]["text"] == "Option 2"
    assert choices[2]["text"] == "Option 3"
    assert choices[3]["text"] == "Option 4"


def test_shortcuts():
    runner.choose(0)

    assert "Option 1 selected." == runner.get_line()
    assert runner.has_line()
    assert "This is the last line." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished
    assert runner.current_node == 'Start'
