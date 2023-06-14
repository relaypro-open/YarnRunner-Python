# YarnRunner-Python

An **unofficial** Python interpreter for compiled [Yarn Spinner](https://yarnspinner.dev/) programs. _Documentation incomplete._

This library currently supports the compiled story format from Yarn Spinner 1.0. The library has also been tested with basic Yarn Spinner 2.0 code, but lacks the implementation for some of 2.0's new features.

## Installation

Right now, the library can be installed directly from source or from [our Releases page](https://github.com/relaypro-open/YarnRunner-Python/releases). We plan to publish the library on PyPi in the near future.

```
pip install git+https://github.com/relaypro-open/YarnRunner-Python@v0.2.5#egg=yarnrunner_python
```

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

As of version v0.0.2, all Yarn Spinner opcodes are currently implemented, as well as Yarn Spinner 1's internal standard library of functions and operators. As of version v0.2.1, typed versions of these functions (introduced in Yarn Spinner 2) are present, but full YS2 parity has not been verified at this time. The known features currently missing are:

- Localisation and Line IDs [(see Yarn's Localization docs)](https://docs.yarnspinner.dev/using-yarnspinner-with-unity/assets-and-localization)
- An appropriate replacement for the distinction Yarn makes between Functions and Coroutines in Unity (to allow users to register blocking command handlers via this Python runner independent of Unity)
- Complete implementation of YS2's type system, specifically when performing operations on mismatching types
  - This may be challenging, due to Python being a dynamically typed language
- The [`<<wait>>` built-in command](https://docs.yarnspinner.dev/getting-started/writing-in-yarn/commands#wait)

## Development

This project uses Python 3 and has a basic test suite.

1. Install dependencies by running `pip install -r requirements.txt`
2. Run `py.test`

To make a release:

1. Make sure you have the latest version of `build` installed:
   > `pip install --upgrade build`
2. Increment the `version` key in `setup.cfg`.
3. Run `python -m build`.

## Updating the protobuf

This project relies on a [Protocol Buffer](https://protobuf.dev/) shared between the Yarn Spinner project and this project to decode compiled Yarn files. Occasionally, this protocol is updated, at which point we must update our implementation. To do this:

1. Pull the latest version of `yarn_spinner.proto` from the YarnSpinner respository [here](https://github.com/YarnSpinnerTool/YarnSpinner/blob/main/YarnSpinner/yarn_spinner.proto).

2. Compile a new verison of the protobuf library. Ensure you have `protoc` installed as described [here](https://grpc.io/docs/protoc-installation/), then, from the root of the respository, run:

```sh
protoc --python_out=yarnrunner_python ./yarn_spinner.proto
```

## Updating the examples

The source code of the examples are located inside `*.yarn` files. `*.csv` and `*.yarnc` files are generated via the Yarn Spinner compiler. To compile these files, follow the below steps:

<details><summary>Yarn Spinner 1</summary>

1. Install the version v0.0.1 of the [Yarn Spinner Console](https://github.com/YarnSpinnerTool/YarnSpinner-Console) program `ysc`. Basic binaries are available on [their releases page](https://github.com/YarnSpinnerTool/YarnSpinner-Console/releases/tag/v0.0.1).
2. From the `examples/yarn1/` directory, compile the examples. For each example, run:

   ```
   ysc compile [filename].yarn
   ```

   - For example, to compile the basic example used in `tests/test_basic.py`, use:

   ```
   ysc compile basic.yarn
   ```

   - This will output `*.csv` and `*.yarnc` files in the current directory, overwriting any files already present with the same name.

</details>
<details open><summary>Yarn Spinner 2</summary>

1. Install the latest version of the [Yarn Spinner Console](https://github.com/YarnSpinnerTool/YarnSpinner-Console) program `ysc`. Basic binaries are available on [their releases page](https://github.com/YarnSpinnerTool/YarnSpinner-Console/releases).
2. From the `examples/yarn2/` directory, compile the examples. For each example, run:

   ```
   ysc compile [filename].yarn -n [filename].yarnc -t [filename].csv
   ```

   - For example, to compile the basic example used in `tests/test_basic.py`, use:

   ```
   ysc compile basic.yarn -n basic.yarnc -t basic.csv
   ```

   - This will output `*.csv` and `*.yarnc` files in the current directory, overwriting any files already present with the same name.

(The long form with multiple CLI arguments used to compile these files is less than ideal. See [YarnSpinnerTool/YarnSpinner-Console#8](https://github.com/YarnSpinnerTool/YarnSpinner-Console/issues/8).)

</details>

Currently `*.csv` and `*.yarnc` files are committed to version control to make it easier to run our test suite. They will likely be gitignored later once we have a better build process for these files.

## License

This project is licensed under the MIT License. See `LICENSE`.
