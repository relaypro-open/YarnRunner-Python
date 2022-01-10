import os
from .context import YarnRunner

compiled_yarn_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/jump.yarnc")
compiled_yarn_f1 = open(compiled_yarn_fname1, "rb")
names_csv_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/jump.csv")
names_csv_f1 = open(names_csv_fname1, "r")
compiled_yarn_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/jump.yarnc"), "rb")
names_csv_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/jump.csv"), "r")

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_start_node_text1():
    assert "This is a test of the jump functionality." == runner1.get_line()
    assert not runner1.has_line()
    assert not runner1.finished


def test_start_node_choices1():
    choices = runner1.get_choices()

    assert len(choices) == 1
    assert choices[0]["choice"] == "begin_jump"
    assert choices[0]["text"] == "Begin Jump"


def test_jumps1():
    runner1.choose(0)

    assert "Some text is output." == runner1.get_line()
    assert runner1.has_line()
    assert "The jump is now complete." == runner1.get_line()
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.current_node == 'jump_complete'


def test_start_node_text2():
    assert "This is a test of the jump functionality." == runner2.get_line()
    assert not runner2.has_line()
    assert not runner2.finished


def test_start_node_choices2():
    choices = runner2.get_choices()

    assert len(choices) == 1
    assert choices[0]["text"] == "Begin Jump"


def test_jumps2():
    runner2.choose(0)

    assert "Some text is output." == runner2.get_line()
    assert runner2.has_line()
    assert "The jump is now complete." == runner2.get_line()
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.current_node == 'jump_complete'


def test_init_repr():
    result = repr(runner1)

    assert result.startswith(
        f"""YarnRunner(open("{compiled_yarn_fname1}", "rb"), open("{names_csv_fname1}"), autostart=True, visits={{'"""
    )

    for v in [
        "'Start': 1",
        "'begin_jump': 1",
        "'jump_stage_2': 1",
        "'jump_complete': 1",
    ]:
        assert v in result

    assert result.endswith("""}, current_node='jump_complete')""")

    result = repr(
        YarnRunner(
            compiled_yarn_f1,
            names_csv_f1,
            autostart=False,
            current_node="jump_stage_2",
            visits={"Start": 1, "begin_jump": 1, "jump_stage_2": 1, "jump_complete": 0},
        )
    )

    assert result.startswith(
        f"""YarnRunner(open("{compiled_yarn_fname1}", "rb"), open("{names_csv_fname1}"), autostart=False, visits={{'"""
    )

    for v in [
        "'Start': 1",
        "'begin_jump': 1",
        "'jump_stage_2': 1",
        "'jump_complete': 0",
    ]:
        assert v in result

    assert "current_node='jump_stage_2'" in result
