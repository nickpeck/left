import logging

import flet as ft

from .app import LeftApp
from .mountedview import MountedView, MountedDialog
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
        MountedDialog(self.page, dialog, **flet_opts)
        logging.getLogger().debug(f"Done mounting dialog")

    def _close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
        self.page.dialog = None
