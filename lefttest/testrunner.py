import inspect
import time
import traceback
from typing import List

from lefttest.testresult import TestResult
from left import LeftApp


class TestRunner:
    results: List[TestResult] = []
    route: str = None
    app: LeftApp

    def __init__(self, app: LeftApp):
        self.app = app
        self._wrap_route_change_handler()

    def _wrap_route_change_handler(self):
        existing_handler = self.app.page.on_route_change

        def _wrapped_handler(*args, **kwargs):
            existing_handler(*args, **kwargs)
            self.route = args[0].route
        self.app.page.on_route_change = _wrapped_handler

    def _reset_database(self):
        self.app.services["database"].drop_tables()
        self.app.services["database"].flush()

    def _before_test(self):
        self._reset_database()

    def _after_test(self):
        pass

    def _before_tests(self):
        self.results = []

    def _after_tests(self):
        self._reset_database()

    def go(self, route: str):
        self.app.page.go(route)
        self._wait_for_route(route)

    def run(self):
        self._before_tests()
        methods = self._get_test_methods()
        for name, f in methods:
            self._run_test(f)
        self._after_tests()
        return self.results

    def _get_test_methods(self):
        methods = inspect.getmembers(self.__class__, predicate=inspect.isfunction)
        methods = list(filter(lambda t: t[0].startswith("test_"), methods))
        return methods

    def _run_test(self, f):
        print(f"================================= {f.__name__}")
        self._before_test()
        try:
            f(self)
            print("PASSED")
            self.results.append(TestResult(test_name=f.__name__, passed=True, stacktrace=""))
        except Exception:
            print("FAILED")
            self.results.append(TestResult(test_name=f.__name__, passed=False, stacktrace=traceback.format_exc()))
        finally:
            self._after_test()

    def _wait_for_route(self, route, max_time=5):
        time_awaited = 0
        while self.route != route:
            if time_awaited >= max_time:
                raise TimeoutError(f"Timeout waiting for {route}")
            time_awaited = time_awaited + 0.1
            time.sleep(0.1)
