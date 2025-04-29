"""
Automated tests. These should be run using
python -m lefttest sampleapp sampleapp.tests
"""

from lefttest.testrunner import TestRunner
import flet as ft


class MyTests(TestRunner):

    def test_create_page_title(self):
        self.go("/page/create")
        assert self.app.page.views[-1].appbar.title.value == 'Create a page'

    def test_index_page_title(self):
        self.go("/")
        assert self.app.page.views[-1].appbar.title.value == 'List Pages'

    def test_create_page(self):
        self.go("/page/create")
        title: ft.Textfield = self.app.page.views[1].controls[1]
        text: ft.Textfield = self.app.page.views[1].controls[2]
        button: ft.ElevatedButton = self.app.page.views[1].controls[3]
        title.value = 'hello'
        text.value = 'world'
        assert button.disabled is True
        text.event_handlers['blur'](ft.ControlEvent(None, None, None, None, self.app.page))
        assert button.disabled is False
        button.event_handlers['click'](ft.ControlEvent('page', 'click', None, button, self.app.page))
        self._wait_for_route("/")
        assert self.app.page.views[-1].appbar.title.value == 'List Pages'
