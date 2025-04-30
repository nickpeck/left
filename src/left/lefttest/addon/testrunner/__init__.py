import os
import sys
import importlib
from inspect import getmembers, isclass
from left import LeftApp
from left.database import TinyDBService
from .controller import ResultsController
from left.lefttest.testrunner import TestRunner

runner: TestRunner = None
results: dict = {}


def on_load(app: LeftApp):
    app.services["database"] = TinyDBService("testing_db.json")
    pass


def on_app_ready(app: LeftApp):
    test_module = os.environ['LEFT_TESTRUNNER_MODULE']
    sys.path.append(test_module)
    test_module = importlib.import_module(test_module)
    global runner
    for _name, cls in getmembers(test_module, isclass):
        if cls == TestRunner:
            continue
        runner = cls(app)
        results[_name] = runner.run()
    app.page.go("/tests/results")
    app.page.update()


def on_route_changed(page, parts):
    match parts:
        case ['tests', 'results']:
            ResultsController(page).results(results)
        case _:
            return
