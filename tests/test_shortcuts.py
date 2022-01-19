import os
from .context import YarnRunner

compiled_yarn_fname1 = os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/shortcuts.yarnc')
compiled_yarn_f1 = open(compiled_yarn_fname1, 'rb')
names_csv_fname1 = os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/shortcuts.csv')
names_csv_f1 = open(names_csv_fname1, 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/shortcuts.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/shortcuts.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_start_node_text1():
    assert "This is a test of shortcut functionality." == runner1.get_line()
    assert not runner1.has_line()
    assert not runner1.finished


def test_start_node_choices1():
    choices = runner1.get_choices()

    assert len(choices) == 4
    assert choices[0]["text"] == "Option 1"
    assert choices[1]["text"] == "Option 2"
    assert choices[2]["text"] == "Option 3"
    assert choices[3]["text"] == "Option 4"


def test_shortcuts1():
    runner1.choose(0)

    assert "Option 1 selected." == runner1.get_line()
    assert runner1.has_line()
    assert "This is the last line." == runner1.get_line()
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.current_node == 'Start'


def test_shortcuts2():
    compiled_yarn_f3 = open(compiled_yarn_fname1, "rb")
    names_csv_f3 = open(names_csv_fname1, "r")
    runner3 = YarnRunner(compiled_yarn_f3, names_csv_f3)
    assert "This is a test of shortcut functionality." == runner3.get_line()
    assert not runner3.has_line()
    assert not runner3.finished
    runner3.choose(1)

    assert "Option 2 selected." == runner3.get_line()
    assert runner3.has_line()
    assert "This is the last line." == runner3.get_line()
    assert not runner3.has_line()
    assert runner3.finished
    assert runner3.current_node == 'Start'


def test_shortcuts3():
    compiled_yarn_f3 = open(compiled_yarn_fname1, "rb")
    names_csv_f3 = open(names_csv_fname1, "r")
    runner3 = YarnRunner(compiled_yarn_f3, names_csv_f3)
    assert "This is a test of shortcut functionality." == runner3.get_line()
    assert not runner3.has_line()
    assert not runner3.finished

    choices = runner3.get_choices()

    assert len(choices) == 4
    assert choices[0]["text"] == "Option 1"
    assert choices[1]["text"] == "Option 2"
    assert choices[2]["text"] == "Option 3"
    assert choices[3]["text"] == "Option 4"

    frozen = repr(runner3)
    runner4 = eval(frozen)

    choices = runner4.get_choices()

    assert len(choices) == 4
    assert choices[0]["text"] == "Option 1"
    assert choices[1]["text"] == "Option 2"
    assert choices[2]["text"] == "Option 3"
    assert choices[3]["text"] == "Option 4"

    runner4.choose(0)

    assert "Option 1 selected." == runner4.get_line()
    assert runner4.has_line()
    assert "This is the last line." == runner4.get_line()
    assert not runner4.has_line()
    assert runner4.finished
    assert runner4.current_node == 'Start'


def test_start_node_text2():
    assert "This is a test of shortcut functionality." == runner2.get_line()
    assert not runner2.has_line()
    assert not runner2.finished


def test_start_node_choices2():
    choices = runner2.get_choices()

    assert len(choices) == 4
    assert choices[0]["text"] == "Option 1"
    assert choices[1]["text"] == "Option 2"
    assert choices[2]["text"] == "Option 3"
    assert choices[3]["text"] == "Option 4"


def test_shortcuts():
    runner2.choose(0)

    assert "Option 1 selected." == runner2.get_line()
    assert runner2.has_line()
    assert "This is the last line." == runner2.get_line()
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.current_node == 'Start'
