from typing import List

from left import LeftRouter

from .pages.controller import PageController


def on_route_change(page, parts: List[str]):
    match parts:
        case ['']:
            PageController(page).index()
        case ['page', 'create']:
            PageController(page).create()
        case ['page', 'view', uid]:
            PageController(page).view(uid)
        case ['page', 'update', uid]:
            PageController(page).update(uid)
        case ['page', 'delete', uid]:
            PageController(page).delete(uid)
        case _:
            print(f"Unrecognised route: {page.route}")
