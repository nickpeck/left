import logging
from typing import List

import flet as ft


class FTRouter:
    """Single-page application router. Use this to load different views as the page route changes."""
    def __init__(self, page):
        self.page = page
        self.page.on_route_change = self._handle_route_change
        self.page.on_view_pop = self._handle_view_pop
        self.page.go(self.page.route)

    def _handle_route_change(self, r: ft.RouteChangeEvent):
        logging.getLogger().info(f"handle_route_change: {r.page.route}")
        if len(self.page.views) > 0:
            if self.page.route == self.page.views[-1].route:
                return
        route = self.page.route
        if route.startswith("/"):
            route = route[1:]
        parts = route.split('/')
        self.on_route_change(parts)
        self.page.update()

    def _handle_view_pop(self, _view: ft.ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def on_route_change(self, parts: List[str]):
        """Use this to call the required controller method as the route changes"""
        raise NotImplementedError()

