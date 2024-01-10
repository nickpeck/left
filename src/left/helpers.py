from typing import List, Callable, Dict, Any
from .app import FTApp


def make_props(*functions):
    """A little helper that converts a list of named functions into a dictionary of {name:function...}
    Useful for functions that take **kwargs"""
    return {f.__name__: f for f in functions}


def redirect(route: str):
    FTApp.get_app().page.go(route)
