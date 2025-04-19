import logging

import flet as ft

from .app import LeftApp
from .mountedview import MountedView
from .view import LeftView, LeftDialog


class LeftController:
    def __init__(self, page: ft.Page):
        self.page = page

    def _mount_view(self, view: LeftView, layered=False, **flet_opts):
        """Mount the view as a new on top of to the current page.
        The view will automatically re-render update whenever view.update_state() is invoked"""
        logging.getLogger().debug(f"mounting view {view} to route {self.page.route}")
        mounted = MountedView(self.page, view, layered, **flet_opts)
        LeftApp.get_app().view_pop_observers.append(mounted.view_was_popped)
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

        MountedView._wrap(method_wrapper, dialog, dialog.update_state.__name__)
        self.page.open(ft_dialog)
        self.page.update()
        logging.getLogger().debug(f"Done mounting dialog")

    def _close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
        self.page.dialog = None
