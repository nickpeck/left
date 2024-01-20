import logging
from typing import Optional, Callable, List

import flet as ft

from .router import LeftRouter


class LeftApp:
    __instance__ = None

    @staticmethod
    def get_app():
        return LeftApp.__instance__

    def __init__(self, router_func: Callable[[List[str]], ...],
                 services: Optional[dict] = None,
                 pre_startup_hook = lambda self: None,
                 **kwargs):
        if LeftApp.__instance__ is not None:
            raise Exception("App already initialized!")
        LeftApp.__instance__ = self
        self.services = {}
        if services is not None:
            self.services.update(services)
        self.page = None
        self.router_func = router_func
        self.opts = kwargs
        self.view_pop_observers = []
        self.pre_startup_hook = pre_startup_hook
        self.ft_app = ft.app(target=self, view=self.opts.get("flet_mode", ft.AppView.FLET_APP))

    def __call__(self, page: ft.Page):
        self.page = page
        self.page.title = self.opts.get("default_title", "Title")
        self.page.theme_mode = self.opts.get("default_theme_mode", ft.ThemeMode.DARK)
        self.page.padding = self.opts.get("default_page_padding", 50)
        self.page.update()
        logging.getLogger().info("App is initialized and ready to serve")
        self.pre_startup_hook(self)
        self.start_routing()

    def start_routing(self):
        LeftRouter(self.page, self.view_was_popped, self.router_func)

    def view_was_popped(self, view: ft.View):
        for observer in self.view_pop_observers:
            observer(view)
