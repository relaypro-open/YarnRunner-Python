import os
from .context import YarnRunner

compiled_yarn_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/conditionals.yarnc")
compiled_yarn_f1 = open(compiled_yarn_fname1, "rb")
names_csv_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/conditionals.csv")
names_csv_f1 = open(names_csv_fname1, "r")
compiled_yarn_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/conditionals.yarnc"), "rb",)
names_csv_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/conditionals.csv"), "r")

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1, autostart=False)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2, autostart=False)


def test_start_node_text1():
    runner1.debug_program_proto()
    runner1.resume()

    assert "This is a test of conditionals and variables." == runner1.get_line()
    assert runner1.has_line()


def test_start_node_text2():
    runner2.debug_program_proto()
    runner2.resume()

    assert "This is a test of conditionals and variables." == runner2.get_line()
    assert runner2.has_line()


def test_conditional_traversal1():
    choices = runner1.get_choices()

    assert len(choices) == 0

    assert "This node should be reached." == runner1.get_line()
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.current_node == 'var_is_2'


def test_conditional_traversal2():
    choices = runner2.get_choices()

    assert len(choices) == 0

    assert "This node should be reached." == runner2.get_line()
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.current_node == 'var_is_2'
