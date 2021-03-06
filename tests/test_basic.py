import os
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/basic.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/basic.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/basic.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/basic.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_start_node_text1():
    assert "This is the first node." == runner1.get_line()
    assert not runner1.has_line()
    assert not runner1.finished


def test_start_node_text2():
    assert "This is the first node." == runner2.get_line()
    assert not runner2.has_line()
    assert not runner2.finished


def test_start_node_choices1():
    choices = runner1.get_choices()

    assert len(choices) == 2
    assert choices[0]["choice"] == "choice_1"
    assert choices[1]["choice"] == "choice_2"
    assert choices[0]["text"] == "Choice 1"
    assert choices[1]["text"] == "Choice 2"


def test_start_node_choices2():
    choices = runner2.get_choices()

    assert len(choices) == 2
    assert choices[0]["text"] == "Choice 1"
    assert choices[1]["text"] == "Choice 2"


side_effect1 = None
side_effect2 = None


def run_a_command1(arg1, arg2, arg3):
    global side_effect1
    side_effect1 = arg3


def run_a_command2(arg1, arg2, arg3):
    global side_effect2
    side_effect2 = (arg1, arg2, arg3)
    return arg3


runner1.add_command_handler("runACommand", run_a_command1)
runner2.add_command_handler("runACommand", run_a_command2)


def test_start_node_choose1():
    runner1.choose(0)

    assert "Here is the node visited as a **result** of the __first__ \"choice\", with a comma." == runner1.get_line()
    assert not runner1.has_line()
    assert runner1.finished

    # ensure the command has run
    assert side_effect1 == "event:/event/event_name"


def test_start_node_choose2():
    runner2.choose(0)

    assert "Here is the node visited as a **result** of the __first__ \"choice\", with a comma." == runner2.get_line()
    assert runner2.has_line()
    assert "spaces and /special &chars" == runner2.get_line()
    assert not runner2.has_line()
    assert runner2.finished

    # ensure the command has run
    assert side_effect2 == ("arg1", "2", "spaces and /special &chars")
