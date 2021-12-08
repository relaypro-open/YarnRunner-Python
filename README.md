# YarnRunner-Python

An **unofficial** Python interpreter for compiled [Yarn Spinner](https://yarnspinner.dev/) programs. _Documentation incomplete._

#### Using the library

Here's an example illustrating how to use the library:

```py
from yarnrunner_python import YarnRunner

# Open the compiled story and strings CSV.
story_f = open('story.yarnc', 'rb')
strings_f = open('story.csv', 'r')

# Create the runner
runner = YarnRunner(story_f, strings_f, autostart=False)

# Register any command handlers
# (see https://yarnspinner.dev/docs/writing/nodes-and-content/#commands)
def custom_command(arg1, arg2):
    pass

runner.add_command_handler("customCommand", custom_command)

# Start the runner and run until you hit a choice point
runner.resume()

# Access the lines printed from the story
print('\n'.join(runner.get_lines()))

# Access the choices
for choice in runner.get_choices():
    print(f"[{choice.index}] ${choice.text}")

# Make a choice and run until the next choice point or the end
runner.choose(0)

# Access the new lines printed from the last run
print('\n'.join(runner.get_lines()))

# Are we done?
if runner.finished:
    print("Woohoo! Our story is over!")
```

A few gotchas to look out for:

- Calling `runner.get_lines()` or `runner.get_line()` is a destructive operation, it fetches the current lines (or line) from the line buffer and then pops them from the buffer. Therefore, calling `runner.get_lines()` twice in a row without making a choice will give you different results. **Feedback on this approach is welcome!**
- Make sure to open the compiled story file as a binary file (see the above example, use `open(filename, 'rb')`) in order for it to be properly parsed by the compiled protobuf library.
- Unless you pass `autostart=False` to the runner when creating it, it will automatically start and run to the next choice point.

Only a subset of Yarn Spinner opcodes are currently implemented. This will certainly change over time. The current status is:

| OpCode           | Status                                                 |
| ---------------- | ------------------------------------------------------ |
| `JUMP_TO`        | ✅&nbsp;&nbsp;Implemented in `runner.__jump_to`        |
| `JUMP`           | ✅&nbsp;&nbsp;Implemented in `runner.__jump`           |
| `RUN_LINE`       | ✅&nbsp;&nbsp;Implemented in `runner.__run_line`       |
| `RUN_COMMAND`    | ✅&nbsp;&nbsp;Implemented in `runner.__run_command`    |
| `ADD_OPTION`     | ✅&nbsp;&nbsp;Implemented in `runner.__add_option`     |
| `SHOW_OPTIONS`   | ✅&nbsp;&nbsp;Implemented in `runner.__show_options`   |
| `PUSH_STRING`    | 🚫&nbsp;&nbsp;Not Implemented                          |
| `PUSH_FLOAT`     | ✅&nbsp;&nbsp;Implemented in `runner.__push_float`     |
| `PUSH_BOOL`      | 🚫&nbsp;&nbsp;Not Implemented                          |
| `PUSH_NULL`      | 🚫&nbsp;&nbsp;Not Implemented                          |
| `JUMP_IF_FALSE`  | ✅&nbsp;&nbsp;Implemented in `runner.__jump_if_false`  |
| `POP`            | ✅&nbsp;&nbsp;Implemented in `runner.__pop`            |
| `CALL_FUNC`      | ✅&nbsp;&nbsp;Implemented in `runner.__call_func`      |
| `PUSH_VARIABLE`  | ✅&nbsp;&nbsp;Implemented in `runner.__push_variable`  |
| `STORE_VARIABLE` | ✅&nbsp;&nbsp;Implemented in `runner.__store_variable` |
| `STOP`           | ✅&nbsp;&nbsp;Implemented in `runner.__stop`           |
| `RUN_NODE`       | ✅&nbsp;&nbsp;Implemented in `runner.__run_node`       |

## Development

This project uses Python 3 and has a basic test suite.

1. Install dependencies by running `pip install -r requirements.txt`
2. Run `py.test`

To make a release:

1. Make sure you have the latest version of `build` installed:
   > `pip install --upgrade build`
2. Increment the `version` key in `setup.cfg`.
3. Run `python -m build`.

## Updating the examples

The source code of the examples are located inside `*.yarn` files. `*.csv` and `*.yarnc` files are generated via the Yarn Spinner compiler. To compile these files, follow the below steps:

1. Install the [Yarn Spinner Console](https://github.com/YarnSpinnerTool/YarnSpinner-Console) program `ysc`. Basic binaries are available on [their releases page](https://github.com/YarnSpinnerTool/YarnSpinner-Console/releases).
2. From the `examples/` directory, run `ysc compile [filename].yarn`. For example, to compile the basic example used in `tests/test_basic.py`, use `ysc compile basic.yarn`.
   - This will output `*.csv` and `*.yarnc` files in the current directory, overwriting any files already present with the same name.

Currently `*.csv` and `*.yarnc` files are committed to version control to make it easier to run our test suite. They will likely be gitignored later once we have a better build process for these files.
