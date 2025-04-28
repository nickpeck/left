from .controller import ResultsController
from .testrunner import TestRunner
from left import LeftApp

runner: TestRunner = None


def on_load(_app: LeftApp):
    pass


def on_app_ready(_app: LeftApp):
    from .tests import MyTests
    global runner
    runner = MyTests(_app)
    runner.run()


def on_route_changed(page, parts):
    global runner
    match parts:
        case ['tests', 'results']:
            ResultsController(page).results(runner.results)
        case _:
            return
