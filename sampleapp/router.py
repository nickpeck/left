from typing import List

from left import LeftRouter

from .pages.controller import PageController


async def on_route_change(page, parts: List[str]):
    match parts:
        case ['']:
            await PageController(page).index()
        case ['page', 'create']:
            await PageController(page).create()
        case ['page', 'view', uid]:
            await PageController(page).view(uid)
        case ['page', 'update', uid]:
            await PageController(page).update(uid)
        case ['page', 'delete', uid]:
            await PageController(page).delete(uid)
        case _:
            print(f"Unrecognised route: {page.route}")
