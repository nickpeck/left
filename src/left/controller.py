import logging

import flet as ft

from .app import LeftApp
from .view import LeftView, LeftDialog


class LeftController:
    @staticmethod
    def _wrap(wrapper, instance, method_name):
        class_method = getattr(instance, method_name)
        wrapped_method = wrapper(class_method)
        setattr(instance, method_name, wrapped_method)

    def __init__(self, page: ft.Page):
        self.page = page

    def _mount_view(self, view: LeftView, layered=False, **flet_opts):
        """Mount the view as a new on top of to the current page.
        The view will automatically re-render update whenever view.update_state() is invoked"""
        logging.getLogger().debug(f"mounting view {view} to route {self.page.route}")

        default_opts = {
            "appbar": view.appbar,
            "controls": view.controls,
            "drawer": view.drawer,
            "end_drawer": view.end_drawer,
            "floating_action_button": view.floating_action_button,
            "route": self.page.route
        }
        flet_opts.update(default_opts)
        ft_view = ft.View(**flet_opts)

        def view_was_popped(popped_view: ft.View):
            if popped_view == ft_view:
                view.on_view_removed()

        def method_wrapper(func_update_state):
            def method_wrap(*args, **kwargs):
                logging.getLogger().debug(f"update_state called on {view}")
                func_update_state(*args, **kwargs)
                ft_view.appbar = view.appbar
                ft_view.controls = view.controls
                ft_view.drawer = view.drawer
                ft_view.end_drawer = view.end_drawer
                ft_view.bottom_appbar = view.bottom_appbar
                logging.getLogger().debug(f"updating view {view}")
                ft_view.update()
            return method_wrap

        self._wrap(method_wrapper, view, view.update_state.__name__)
        if not layered:
            self.page.views.clear()
        self.page.views.append(ft_view)
        self.page.update()
        LeftApp.get_app().view_pop_observers.append(view_was_popped)
        logging.getLogger().debug(f"Done mounting view")

    def _mount_dialog(self, dialog: LeftDialog, **flet_opts):
        logging.getLogger().debug(f"mounting dialog {dialog} to page {self.page}")

        default_opts = {
            "title": dialog.title,
            "content": dialog.content,
            "actions": dialog.actions
        }
        flet_opts.update(default_opts)
        ft_dialog = ft.AlertDialog(**flet_opts)

        def method_wrapper(func_update_state):
            def method_wrap(*args, **kwargs):
                logging.getLogger().debug(f"update_state called on {dialog}")
                func_update_state(*args, **kwargs)
                ft_dialog.content = dialog.content
                ft_dialog.actions = dialog.actions
                logging.getLogger().debug(f"updating view {dialog}")
                ft_dialog.update()

            return method_wrap

        self._wrap(method_wrapper, dialog, dialog.update_state.__name__)
        self.page.dialog = ft_dialog
        self.page.dialog.open = True
        self.page.update()
        logging.getLogger().debug(f"Done mounting dialog")

    def _close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
        self.page.dialog = None
