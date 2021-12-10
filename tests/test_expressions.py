import os
from .context import YarnRunner

compiled_yarn_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/expressions.yarnc'), 'rb')
names_csv_f = open(os.path.join(os.path.dirname(
    __file__), '../examples/expressions.csv'), 'r')

runner = YarnRunner(compiled_yarn_f, names_csv_f, autostart=False)

# TODO: implement a test for expression parsing


def test_expressions():
    try:
        runner.resume()

        # the runner should throw an error
        raise Exception(
            "The runner ran without any issues. This test should fail. An Exception was expected.")
    except Exception as e:
        assert str(
            e) == "Yarn stories with interpolated inline expressions are not yet supported."
