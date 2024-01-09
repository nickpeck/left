import logging

import flet as ft


class FTController:
    def __init__(self, page: ft.Page):
        self.page = page

    def _mount_view(self, view: ft.View, **flet_opts):
        """Mount the view as a new on top of to the current page.
        The view will automatically re-render update whenever view.update_state() is invoked"""
        logging.getLogger().debug(f"mounting view {view} to route {self.page.route}")

        default_opts = {
            "appbar": view.get_appbar(),
            "controls": view.get_controls()
        }
        flet_opts.update(default_opts)
        ft_view = ft.View(**flet_opts)

        def method_wrapper(func_update_state):
            def method_wrap(*args, **kwargs):
                logging.getLogger().debug(f"update_state called on {view}")
                func_update_state(*args, **kwargs)
                ft_view.appbar = view.get_appbar()
                ft_view.controls = view.get_controls()
                logging.getLogger().debug(f"updating view {view}")
                ft_view.update()
            return method_wrap

        def _wrap(wrapper, instance, method):
            class_method = getattr(instance, method)
            wrapped_method = wrapper(class_method)
            setattr(instance, method, wrapped_method)

        _wrap(method_wrapper, view, "update_state")
        self.page.views.append(ft_view)
        self.page.update()
        logging.getLogger().debug(f"Done mounting view")
