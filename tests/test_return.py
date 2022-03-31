import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/return.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/return.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f, autostart=False)


def return_command():
    runner.climb_node_stack()


runner.add_command_handler("return", return_command)


def test_return():
    runner.resume()
    assert "Here's an example of returning inline from a node." == runner.get_line()
    assert runner.has_line()
    assert "Here's the inline node." == runner.get_line()
    assert runner.has_line()
    assert "Here's the last line." == runner.get_line()
    assert not runner.has_line()
    assert runner.finished
