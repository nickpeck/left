import unittest
from unittest import mock

import flet as ft

from left.router import LeftRouter


class TestRouter(unittest.TestCase):
    def test_router_redirects_to_current_route(self):
        page = mock.Mock()
        page.route = "/"
        page.go = mock.Mock()
        LeftRouter(page, lambda parts: page.go("/"))
        assert page.go.call_args == mock.call("/")

    def test_handle_route_change(self):
        page = mock.Mock()
        page.route = "/"
        page.go = mock.Mock()
        page.views = []
        on_route_change = mock.Mock()
        router = LeftRouter(page, on_route_change)
        page.on_route_change(ft.RouteChangeEvent(route="/new/route"))
        assert on_route_change.call_args == mock.call(page, ['new', 'route'])

    def test_handle_view_pop(self):
        page = mock.Mock()
        page.route = "/"
        page.go = mock.Mock()
        LeftRouter(page, mock.Mock())
        page.views = [ft.View(route="/earlier-route"), ft.View(route="/latest-route")]
        page.on_view_pop(ft.ViewPopEvent(page.views[-1]))
        assert page.route == "/earlier-route"


if __name__ == '__main__':
    unittest.main()
