import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/conditionals.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/conditionals.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f, autostart=False)


def test_start_node_text():
    runner.debug_program_proto()
    runner.resume()

    assert "This is a test of conditionals and variables." == runner.get_line()
    assert runner.has_line()


def test_conditional_traversal():
    choices = runner.get_choices()

    assert len(choices) == 0

    assert "This node should be reached." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished
    assert runner.current_node == 'var_is_2'
