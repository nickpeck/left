from .app import LeftApp


def make_props(*functions):
    """A little helper that converts a list of named functions into a dictionary of {name:function...}
    Useful for functions that take **kwargs"""
    return {f.__name__: f for f in functions}


def redirect(route: str):
    LeftApp.get_app().page.go(route)


def get_page():
    return LeftApp.get_app().page
