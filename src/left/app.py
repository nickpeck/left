import logging
from typing import Optional

import flet as ft

from .router import FTRouter


class FTApp:
    __instance__ = None

    @staticmethod
    def get_app():
        return FTApp.__instance__

    def __init__(self, router_cls: FTRouter = FTRouter, services: Optional[dict] = None, **kwargs):
        if FTApp.__instance__ is not None:
            raise Exception("App already initialized!")
        FTApp.__instance__ = self
        self.services = {}
        if services is not None:
            self.services.update(services)
        self.page = None
        self.router_cls = router_cls
        self.opts = kwargs
        ft.app(target=self, view=self.opts.get("flet_mode", ft.AppView.FLET_APP))

    def __call__(self, page: ft.Page):
        self.page = page
        self.page.title = self.opts.get("default_title", "Title")
        self.page.theme_mode = self.opts.get("default_theme_mode", ft.ThemeMode.DARK)
        self.page.padding = self.opts.get("default_page_padding", 50)
        self.page.update()
        logging.getLogger().info(f"App is initialized and ready to serve")
        self.start_routing()

    def start_routing(self):
        self.router_cls(self.page)
