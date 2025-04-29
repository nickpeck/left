import os
import sys

import logging
import importlib


class Addons:
    """
    used to manage the lifecycle of addon modules, which are defined at LEFT_ADDON_PATH (default addons)
    """

    def __init__(self):
        self.addons = self.load_addons()
        self.call_addon_hook("on_load", self)

    @staticmethod
    def load_addons():
        addons = []
        addon_paths = os.environ.get("LEFT_ADDON_PATH", "addons").split(';')
        for addon_path in addon_paths:
            if not os.path.exists(addon_path):
                continue
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

    def __iter__(self):
        return iter(self.addons)
