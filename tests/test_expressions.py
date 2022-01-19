import os
from .context import YarnRunner

compiled_yarn_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/expressions.yarnc'), 'rb')
names_csv_f1 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn1/expressions.csv'), 'r')
compiled_yarn_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/expressions.yarnc'), 'rb')
names_csv_f2 = open(os.path.join(os.path.dirname(
    __file__), '../examples/yarn2/expressions.csv'), 'r')

runner1 = YarnRunner(compiled_yarn_f1, names_csv_f1, autostart=False)
runner2 = YarnRunner(compiled_yarn_f2, names_csv_f2, autostart=False)

# TODO: implement a test for expression parsing


def test_expressions1():
    try:
        runner1.resume()

        # the runner should throw an error
        raise Exception(
            "The runner ran without any issues. This test should fail. An Exception was expected.")
    except Exception as e:
        assert str(
            e) == "Yarn stories with interpolated inline expressions are not yet supported."


def test_expressions2():
    try:
        runner2.resume()

        # the runner should throw an error
        raise Exception(
            "The runner ran without any issues. This test should fail. An Exception was expected.")
    except Exception as e:
        assert str(
            e) == "Yarn stories with interpolated inline expressions are not yet supported."
