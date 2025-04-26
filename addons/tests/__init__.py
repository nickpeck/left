# addons/myaddonmodule/__init__.py
import inspect
import time
import traceback
from threading import Thread

from left import LeftApp, LeftController, LeftView
from left.helpers import redirect
from sampleapp.pages.controller import PageController
import flet as ft

class TestRunner(Thread):
    results = []
        
    def run(self) -> None:
        from time import sleep
        sleep(0.1)
        self.page = LeftApp.get_app().page
        methods = inspect.getmembers(self.__class__, predicate=inspect.isfunction)
        for name, f in methods:
            if name.startswith("test_"):
                print(f"================================= {name}")
                try:
                    f(self)
                except Exception as e:
                    traceback.print_exc()
                    print("FAILED")
                    self.results.append(f"{name}       FAILED")
                    continue
                finally:
                    sleep(2)
                print("PASSED")
                self.results.append(f"{name}       PASSED")
        self.page.go("/tests/results")
        self.page.update()



    def test_create_page_title(self):
        PageController(self.page).create()
        assert self.page.views[-1].appbar.title.value == 'Create a page'



    def test_index_page_title(self):
        PageController(self.page).index()
        assert self.page.views[-1].appbar.title.value == 'List Pages'


    def test_create_page(self):
        self.page.go("/page/create")
        self.page.update()
        time.sleep(0.3)
        title: ft.Textfield = self.page.views[1].controls[1]
        text : ft.Textfield = self.page.views[1].controls[2]
        button : ft.ElevatedButton = self.page.views[1].controls[3]
        title.value = 'hello'
        text.value = 'world'
        assert button.disabled == True
        text.event_handlers['blur'](ft.ControlEvent(None, None, None, None, self.page))
        assert button.disabled == False
        button.event_handlers['click'](ft.ControlEvent('page', 'click', None, button, self.page))
        self.page.update()
        time.sleep(0.3)
        assert self.page.views[-1].appbar.title.value == 'List Pages'


runner = TestRunner()



class ResultsView(LeftView):

    def __init__(self):
        self.state = {'results': []}

    @property
    def controls(self):
        return [
            ft.Column(
                controls=[ft.Row(
                    controls=[
                        ft.Text(result)
                    ]
                ) for result in self.state['results']]
            )
        ]




class ResultsController(LeftController):

    def results(self):
        print("GOT HERE!!!!!")
        view = ResultsView()
        self._mount_view(view)
        view.update_state(results=runner.results)


def on_load(_app: LeftApp):
    # any actions to be taken on load, ie storing settings in the db
    pass


def on_app_ready(_app: LeftApp):
    runner.start()
    pass


def on_route_changed(page, parts):
    match parts:
        case ['tests', 'results']:
            ResultsController(page).results()
        case _:
            return