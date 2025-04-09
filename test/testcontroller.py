import unittest
from unittest import TestCase, mock

from left.controller import LeftController
from left.view import LeftView, LeftDialog


class TestController(TestCase):

    @mock.patch("left.app.LeftApp.get_app", new_callable=mock.PropertyMock)
    def test_can_mount_view(self, _get_app):
        page = mock.Mock()
        view = LeftView()
        controller = LeftController(page)
        controller._mount_view(view)

    @mock.patch("left.app.LeftApp.get_app", new_callable=mock.PropertyMock)
    @mock.patch("left.view.LeftView.controls", new_callable=mock.PropertyMock)
    def test_mounted_view_redraws_when_state_changed(self, controls, _get_app):
        page = mock.Mock()
        view = LeftView()
        controller = LeftController(page)
        controller._mount_view(view)
        assert controls.called
        controls.called = False
        view.update_state(**{"foo": "bar"})
        assert controls.called

    @mock.patch("left.view.LeftDialog.content", new_callable=mock.PropertyMock)
    @mock.patch("left.view.LeftDialog.actions", new_callable=mock.PropertyMock)
    def test_can_mount_dialog(self, content, actions):
        page = mock.Mock()
        dialog = LeftDialog()
        controller = LeftController(page)
        controller._mount_dialog(dialog)
        assert content.called
        assert actions.called


if __name__ == '__main__':
    unittest.main()
