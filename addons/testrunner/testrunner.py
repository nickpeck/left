import inspect
import time
import traceback

from left import LeftApp
import flet as ft

from left.database.tinydbservice import TinyDBService


class TestRunner:
    results = []
    route: str = None
    app: LeftApp

    def __init__(self, app: LeftApp):
        self.app = app
        self.page = app.page
        self._bind_route_change_handler()
        self.app.services["database"] = TinyDBService("testing_db.json",  write_through=False)

    def _bind_route_change_handler(self):
        existing_handler = self.page.on_route_change
        def new_handler(*args, **kwargs):
            existing_handler(*args, **kwargs)
            self.route = args[0].route
        self.page.on_route_change = new_handler


    def setUp(self):
        self.app.services["database"].drop_tables()
        self.app.services["database"].flush()


    def tearDown(self):
        pass


    def run(self) -> None:
        from time import sleep
        try:
            self._wait_for_app("/", max_time=10)
        except TimeoutError:
            print("App did not initialise within 10 seconds")
            exit(1)

        methods = inspect.getmembers(self.__class__, predicate=inspect.isfunction)
        for name, f in methods:
            if name.startswith("test_"):
                print(f"================================= {name}")
                self.setUp()
                try:
                    f(self)
                except Exception as e:
                    traceback.print_exc()
                    print("FAILED")
                    self.results.append(f"{name}       FAILED")
                    continue
                finally:
                    sleep(2)
                    self.tearDown()
                print("PASSED")
                self.results.append(f"{name}       PASSED")
        self.page.go("/tests/results")
        self.page.update()


    def _wait_for_app(self, route, max_time=5):
        time_awaited = 0
        while self.route != route:
            if time_awaited >= max_time:
                raise TimeoutError(f"Timeout waiting for {route}")
            time_awaited = time_awaited + 0.1
            time.sleep(0.1)


    def test_create_page_title(self):
        self.page.go("/page/create")
        self._wait_for_app("/page/create")
        assert self.page.views[-1].appbar.title.value == 'Create a page'



    def test_index_page_title(self):
        self.page.go("/")
        self._wait_for_app("/")
        assert self.page.views[-1].appbar.title.value == 'List Pages'


    def test_create_page(self):
        self.page.go("/page/create")
        self._wait_for_app("/page/create")
        title: ft.Textfield = self.page.views[1].controls[1]
        text : ft.Textfield = self.page.views[1].controls[2]
        button : ft.ElevatedButton = self.page.views[1].controls[3]
        title.value = 'hello'
        text.value = 'world'
        assert button.disabled == True
        text.event_handlers['blur'](ft.ControlEvent(None, None, None, None, self.page))
        assert button.disabled == False
        button.event_handlers['click'](ft.ControlEvent('page', 'click', None, button, self.page))
        self._wait_for_app("/")
        assert self.page.views[-1].appbar.title.value == 'List Pages'
