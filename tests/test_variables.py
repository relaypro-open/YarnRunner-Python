import os
from .context import YarnRunner

compiled_yarn_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/variables.yarnc")
compiled_yarn_f1 = open(compiled_yarn_fname1, "rb")
names_csv_fname1 = os.path.join(os.path.dirname(__file__), "../examples/yarn1/variables.csv")
names_csv_f1 = open(names_csv_fname1, "r")
compiled_yarn_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/variables.yarnc"), "rb")
names_csv_f2 = open(os.path.join(os.path.dirname(__file__), "../examples/yarn2/variables.csv"), "r")

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2)


def test_variables1():
    assert not runner1.has_line()
    assert runner1.finished
    assert runner1.variables["$value_string"] == "string"
    assert runner1.variables["$value_float"] == 1.25
    assert runner1.variables["$value_bool"] == True
    assert runner1.variables["$value_null"] is None


def test_variables2():
    assert not runner2.has_line()
    assert runner2.finished
    assert runner2.variables["$value_string"] == "string"
    assert runner2.variables["$value_float"] == 1.25
    assert runner2.variables["$value_bool"] == True


def test_init_repr():
    result = repr(runner1)

    assert result.startswith(
        f"""YarnRunner(open("{compiled_yarn_fname1}", "rb"), open("{names_csv_fname1}"), autostart=True, visits={{'Start': 1}}, variables={{'"""
    )

    for v in [
        "'$value_string': 'string'",
        "'$value_float': 1.25",
        "'$value_bool': True",
        "'$value_null': None",
    ]:
        assert v in result

    assert result.endswith("""}, current_node='Start')""")

    runner3 = YarnRunner(
        compiled_yarn_f1,
        names_csv_f1,
        autostart=False,
        variables={
            "$value_string": "gnirts",
            "$value_float": 2.75,
            "$value_bool": False,
        },
    )
    result = repr(runner3)

    assert result.startswith(
        f"""YarnRunner(open("{compiled_yarn_fname1}", "rb"), open("{names_csv_fname1}"), autostart=False, variables={{'"""
    )

    for v in [
        "'$value_string': 'gnirts'",
        "'$value_float': 2.75",
        "'$value_bool': False",
    ]:
        assert v in result
