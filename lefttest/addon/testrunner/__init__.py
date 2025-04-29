import os
import sys
import importlib
from inspect import getmembers, isclass
from left import LeftApp
from .controller import ResultsController
from .testrunner import TestRunner

runner: TestRunner = None


def on_load(_app: LeftApp):
    pass


def on_app_ready(_app: LeftApp):
    test_module = os.environ['LEFT_TESTRUNNER_MODULE']
    sys.path.append(test_module)
    test_module = importlib.import_module(test_module)
    global runner
    for _name, cls in getmembers(test_module, isclass):
        runner = cls(_app)
        runner.run()


def on_route_changed(page, parts):
    global runner
    match parts:
        case ['tests', 'results']:
            ResultsController(page).results(runner.results)
        case _:
            return
