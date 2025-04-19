import logging

from left import LeftView
import flet as ft
from typing import Optional


class MountedView:
    ft_view: Optional[ft.View] = None
    view: Optional[LeftView] = None
    page: Optional[ft.Page] = None

    def __init__(self, page: ft.Page, view: LeftView, layered=False, **flet_opts):
        self.page = page
        self.view = view
        flet_opts = self._init_view_options(flet_opts, view)
        self.ft_view = ft.View(**flet_opts)
        self._wrap(self.method_wrapper, view, view.update_state.__name__)
        if not layered:
            self.page.views.clear()
        self.page.views.append(self.ft_view)
        self.page.update()

    @staticmethod
    def _wrap(wrapper, instance, method_name):
        class_method = getattr(instance, method_name)
        wrapped_method = wrapper(class_method)
        setattr(instance, method_name, wrapped_method)

    def _init_view_options(self, flet_opts, view):
        default_opts = {
            "appbar": view.appbar,
            "controls": view.controls,
            "drawer": view.drawer,
            "end_drawer": view.end_drawer,
            "floating_action_button": view.floating_action_button,
            "route": self.page.route
        }
        flet_opts.update(default_opts)
        return flet_opts

    def view_was_popped(self, popped_view: ft.View):
        if popped_view == self.ft_view:
            self.view.on_view_removed()

    def _rebuild_view_controls(self):
        self.ft_view.appbar = self.view.appbar
        self.ft_view.controls = self.view.controls
        self.ft_view.drawer = self.view.drawer
        self.ft_view.end_drawer = self.view.end_drawer
        self.ft_view.bottom_appbar = self.view.bottom_appbar

    def method_wrapper(self, func_update_state):
        def method_wrap(*args, **kwargs):
            logging.getLogger().debug(f"update_state called on {self.view}")
            func_update_state(*args, **kwargs)
            self._rebuild_view_controls()
            logging.getLogger().debug(f"updating view {self.view}")
            self.page.update()
        return method_wrap

