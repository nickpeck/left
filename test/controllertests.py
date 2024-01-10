import unittest
from unittest import TestCase, mock

import flet

from left.controller import LeftController
from left.view import LeftView


class TestController(TestCase):

    def test_can_mount_view(self):
        page = mock.Mock()
        view = LeftView()
        controller = LeftController(page)
        controller._mount_view(view)

    @mock.patch("left.view.LeftView.controls", new_callable=mock.PropertyMock)
    @mock.patch("flet.View")
    def test_mounted_view_redraws_when_state_changed(self, ft_view, controls):
        page = mock.Mock()
        view = LeftView()
        controller = LeftController(page)
        controller._mount_view(view)
        assert controls.called
        controls.called = False
        view.update_state(**{"foo": "bar"})
        assert controls.called


if __name__ == '__main__':
    unittest.main()
