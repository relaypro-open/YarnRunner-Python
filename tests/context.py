import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# the "nopep8" is to ensure this is below "sys.path", autopep8 will autoformat it above otherwise
from yarnrunner_python import YarnRunner  # nopep8

# for the structure of this file, see https://docs.python-guide.org/writing/structure/#test-suite
