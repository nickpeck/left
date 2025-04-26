from __future__ import annotations
import logging
from typing import Optional, Callable, List

import flet as ft

from .router import LeftRouter
from .addons import Addons


class LeftApp:
    __instance__: Optional[LeftApp] = None
    page: Optional[ft.Page] = None

    @staticmethod
    def get_app():
        return LeftApp.__instance__

    def __init__(self, router_func: Callable[[List[str]], ...],
                 services: Optional[dict] = None,
                 pre_startup_hook=lambda self: None,
                 **kwargs):
        if LeftApp.__instance__ is not None:
            raise Exception("App already initialized!")
        LeftApp.__instance__ = self
        self.opts = kwargs
        self.services = services if services else {}
        self.router_func = router_func
        self.view_pop_observers = []
        self.addons = Addons()
        self.pre_startup_hook = pre_startup_hook
        self.splash_screen = self._load_splashscreen() if self.opts.get("splash_image") else None
        ft.app(target=self, view=self.opts.get("flet_mode", ft.AppView.FLET_APP))

    def __call__(self, page: ft.Page):
        # workaround for window failing to restore from background https://github.com/flet-dev/flet/issues/2951
        # https://flet.dev/docs/controls/page/#on_window_event
        async def on_window_event(_):
            page.window_height = page.window_max_height
            page.window_width = page.window_max_width
            page.window_top = 10
            page.window_left = 10
            await page.update_async()

        self._init_page(page)
        logging.getLogger().info("App is initialized and ready to serve")
        self.pre_startup_hook(self)
        if self.splash_screen is not None:
            self.splash_screen.close_splash()
        self.start_routing()

    def _init_page(self, page):
        self.page = page
        self.page.window.prevent_close = True
        self.page.window.on_event = self.on_window_event
        self.page.title = self.opts.get("default_title", "Title")
        self.page.theme_mode = self.opts.get("default_theme_mode", ft.ThemeMode.DARK)
        self.page.padding = self.opts.get("default_page_padding", 50)
        self.page.update()

    def start_routing(self):
        addon_routers = []
        for addon in self.addons:
            if "on_route_changed" in dir(addon):
                addon_routers.append(addon.on_route_changed)

        def on_route_changed(*args, **kwargs):
            self.router_func(*args, **kwargs)
            for router in addon_routers:
                router(*args, **kwargs)
        LeftRouter(self.page, on_view_popped_cb=self.view_was_popped, on_route_change=on_route_changed)
        self.addons.call_addon_hook("on_app_ready", self)

    def view_was_popped(self, view: ft.View):
        for observer in self.view_pop_observers:
            observer(view)

    def on_window_event(self, e):
        if e.data == "close":
            self.addons.call_addon_hook("on_close", self)
            for _, service in self.services.items():
                service.close()
            self.page.window.destroy()

    def _load_splashscreen(self):
        from .splashscreen import SplashScreen  # optional import, Windows only
        # nb, uses TK, so you will need to package with pyinstaller: 'flet package myapp.py'
        return SplashScreen(
            title=self.opts.get("default_title", "Title"),
            img_path=self.opts.get("splash_image"),
            duration=self.opts.get("splash_duration", 3000))
