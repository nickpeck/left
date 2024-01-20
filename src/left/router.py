import logging
from typing import List, Callable, Optional

import flet as ft


class LeftRouter:
    """Single-page application router. Use this to load different views as the page route changes."""
    def __init__(self, page, on_route_change: Callable[[List[str]], ...],
                 on_view_popped_cb: Optional[Callable[[ft.View], ...]] = None):
        self.page = page
        self.on_route_change = on_route_change
        self.page.on_route_change = self._handle_route_change
        self.page.on_view_pop = self._handle_view_pop
        self.page.go(self.page.route)
        self.on_view_popped_cb = on_view_popped_cb

    def _handle_route_change(self, r: ft.RouteChangeEvent):
        logging.getLogger().info(f"handle_route_change: {r.route}")

        if len(self.page.views) and self.page.route == self.page.views[-1].route:
            # this is a 'back' history action, so no need to re-render the pre-existing previous view.
            return

        route = r.route
        if route.startswith("/"):
            route = route[1:]
        parts = route.split('/')
        self.on_route_change(self.page, parts)

    def _handle_view_pop(self, _view: ft.ViewPopEvent):
        logging.getLogger().info(f"_handle_view_pop view, current list of views is {self.page.views}")
        popped = self.page.views.pop()
        if self.on_view_popped_cb is not None:
            self.on_view_popped_cb(popped)
        self.page.route = self.page.views[-1].route
        self.page.update()
