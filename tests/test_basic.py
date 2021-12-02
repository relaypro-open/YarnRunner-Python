import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/basic.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/basic.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f)


def test_start_node_text():
    assert "This is the first node." == runner.get_line()
    assert not runner.has_line()
    assert not runner.finished


def test_start_node_choices():
    choices = runner.get_choices()

    assert len(choices) == 2
    assert choices[0]["choice"] == "choice_1"
    assert choices[1]["choice"] == "choice_2"
    assert choices[0]["text"] == "Choice 1"
    assert choices[1]["text"] == "Choice 2"


side_effect = None


def run_a_command(arg1, arg2, arg3):
    global side_effect
    side_effect = arg3


runner.add_command_handler("runACommand", run_a_command)


def test_start_node_choose():
    runner.choose(0)

    assert "Here is the node visited as a **result** of the __first__ \"choice\", with a comma." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished

    # ensure the command has run
    assert side_effect == "event:/event/event_name"
