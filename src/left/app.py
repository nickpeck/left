import asyncio
import logging
import os
import sys
from typing import Optional, Callable, List
import importlib

import flet as ft

from .router import LeftRouter


class LeftApp:
    __instance__ = None

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
        self.services = {}
        if services is not None:
            self.services.update(services)
        self.page = None
        self.router_func = router_func
        self.opts = kwargs
        self.view_pop_observers = []
        self.addons = self.load_addons()
        self.call_addon_hook("on_load", self)
        self.pre_startup_hook = pre_startup_hook
        async def f():
            await ft.app_async(target=self, view=self.opts.get("flet_mode", ft.AppView.FLET_APP))

        asyncio.run(f())

    async def __call__(self, page: ft.Page):
        self.page = page
        self.page.window_prevent_close = True
        self.page.on_window_event = self.on_window_event
        self.page.title = self.opts.get("default_title", "Title")
        self.page.theme_mode = self.opts.get("default_theme_mode", ft.ThemeMode.DARK)
        self.page.padding = self.opts.get("default_page_padding", 50)
        await self.page.update_async()
        logging.getLogger().info("App is initialized and ready to serve")
        self.pre_startup_hook(self)
        await self.start_routing()

    async def start_routing(self):
        addon_routers = []
        for addon in self.addons:
            if "on_route_changed" in dir(addon):
                addon_routers.append(addon.on_route_changed)

        async def on_route_changed(*args, **kwargs):
            await self.router_func(*args, **kwargs)
            for router in addon_routers:
                router(*args, **kwargs)
        await LeftRouter(self.page, on_view_popped_cb=self.view_was_popped, on_route_change=on_route_changed)

    def view_was_popped(self, view: ft.View):
        for observer in self.view_pop_observers:
            observer(view)

    @staticmethod
    def load_addons():
        addons = []
        addon_path = os.environ.get("LEFT_ADDON_PATH", "addons")
        if not os.path.exists(addon_path):
            return addons
        sys.path.append(addon_path)
        for _, folder, _ in os.walk(addon_path):
            if len(folder) == 0:
                continue
            if folder[0].startswith("_"):
                continue
            try:
                addon = importlib.import_module(folder[0])
            except ImportError as ie:
                logging.getLogger().error(ie)
                continue
            addons.append(addon)
        return addons

    def call_addon_hook(self, name: str, *args, **kwargs):
        for addon in self.addons:
            if name in dir(addon):
                getattr(addon, name)(*args, **kwargs)

    def get_addon_buttons(self):
        buttons = []
        for addon in self.addons:
            if "main_menu_icon" in dir(addon):
                buttons.append(addon.main_menu_icon())
        return buttons

    async def on_window_event(self, e):
        if e.data == "close":
            self.call_addon_hook("on_close", self)
            for _, service in self.services.items():
                service.close()
            await self.page.window_destroy_async()
