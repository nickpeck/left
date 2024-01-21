from .app import LeftApp

import flet as ft

def make_props(*functions):
    """A little helper that converts a list of named functions into a dictionary of {name:function...}
    Useful for functions that take **kwargs"""
    return {f.__name__: f for f in functions}


def redirect(route: str):
    page = LeftApp.get_app().page
    if page.route == route:
        return
    page.go(route)


def go_back(e):
    """e is an event originating from a control on the active view"""
    page = LeftApp.get_app().page
    page.on_view_pop.get_handler()(e)


def get_page():
    return LeftApp.get_app().page
