import unittest
from unittest import mock

import flet

from left.app import LeftApp
from left.router import LeftRouter


class TestRouter(unittest.TestCase):

    def setUp(self) -> None:
        LeftApp.__instance__ = None

    @mock.patch("flet.app")
    def test_app_initialize(self, app):
        LeftRouter.on_route_change = mock.Mock()
        LeftApp(router=LeftRouter)

    @mock.patch("flet.app")
    def test_app_should_be_callable(self, app):
        LeftRouter.on_route_change = mock.Mock()
        app = LeftApp(router=LeftRouter)
        page = mock.Mock()
        app(page)

    @mock.patch("flet.app")
    def test_cannot_initialize_twice(self, _app):
        LeftRouter.on_route_change = mock.Mock()
        LeftApp(router=LeftRouter)
        with self.assertRaises(Exception):
            LeftApp(router=LeftRouter)


if __name__ == '__main__':
    unittest.main()
