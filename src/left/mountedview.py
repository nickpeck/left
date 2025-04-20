import logging
from abc import ABC, abstractmethod

from left import LeftView
import flet as ft
from typing import Optional

from left.view import LeftDialog, LeftViewBase


class Mounted(ABC):
    """
    Connect a left view to a flet AdaptiveControl, such as that whenever
    update_state() is called on the left view, the actual flet view is refreshed.
    """
    page: ft.Page
    left_view: LeftViewBase

    def _bind_update_state_to_page_update(self, instance):
        method_name = LeftViewBase.update_state.__name__
        class_method = getattr(instance, method_name)
        wrapped_method = self._method_wrapper(class_method)
        setattr(instance, method_name, wrapped_method)

    def _method_wrapper(self, func_update_state):
        def method_wrap(*args, **kwargs):
            logging.getLogger().debug(f"update_state called on {self.left_view}")
            func_update_state(*args, **kwargs)
            self._rebuild_controls()
            logging.getLogger().debug(f"updating view {self.left_view}")
            self.page.update()
        return method_wrap

    @abstractmethod
    def _rebuild_controls(self):
        pass


class MountedView(Mounted):
    """
    Mount a flet.View instance onto the page
    """
    ft_view: Optional[ft.View] = None
    left_view: LeftView

    def __init__(self, page: ft.Page, left_view: LeftView, layered=False, **flet_opts):
        self.page = page
        self.left_view = left_view
        flet_opts = self._init_view_options(flet_opts)
        self.ft_view = ft.View(**flet_opts)
        self._bind_update_state_to_page_update(self.left_view)
        if not layered:
            self.page.views.clear()
        self.page.views.append(self.ft_view)
        self.page.update()

    def _init_view_options(self, flet_opts):
        default_opts = {
            "appbar": self.left_view.appbar,
            "controls": self.left_view.controls,
            "drawer": self.left_view.drawer,
            "end_drawer": self.left_view.end_drawer,
            "floating_action_button": self.left_view.floating_action_button,
            "route": self.page.route
        }
        flet_opts.update(default_opts)
        return flet_opts

    def view_was_popped(self, popped_view: ft.View):
        if popped_view == self.ft_view:
            self.left_view.on_view_removed()

    def _rebuild_controls(self):
        self.ft_view.appbar = self.left_view.appbar
        self.ft_view.controls = self.left_view.controls
        self.ft_view.drawer = self.left_view.drawer
        self.ft_view.end_drawer = self.left_view.end_drawer
        self.ft_view.bottom_appbar = self.left_view.bottom_appbar


class MountedDialog(Mounted):
    """
    Mount a flet AlertDialog onto the active page
    """
    left_view: LeftDialog

    def __init__(self, page: ft.Page, dialog: LeftDialog, **flet_opts):
        self.page = page
        self.left_view = dialog
        flet_opts = self._init_view_options(flet_opts, dialog)
        self.ft_dialog = ft.AlertDialog(**flet_opts)
        self._bind_update_state_to_page_update(dialog)
        page.open(self.ft_dialog)
        page.update()

    @staticmethod
    def _init_view_options(flet_opts, dialog):
        default_opts = {
            "title": dialog.title,
            "content": dialog.content,
            "actions": dialog.actions
        }
        flet_opts.update(default_opts)
        return flet_opts

    def _rebuild_controls(self):
        self.ft_dialog.content = self.left_view.content
        self.ft_dialog.actions = self.left_view.actions
