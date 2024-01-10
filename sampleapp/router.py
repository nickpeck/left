from typing import List

from left import LeftRouter

from .pages.controller import PageController


class MyRouter(LeftRouter):
    def on_route_change(self, parts: List[str]):
        match parts:
            case ['']:
                PageController(self.page).index()
            case ['page', 'create']:
                PageController(self.page).create()
            case ['page', 'view', uid]:
                PageController(self.page).view(uid)
            case ['page', 'update', uid]:
                PageController(self.page).update(uid)
            case ['page', 'delete', uid]:
                PageController(self.page).delete(uid)
            case _:
                print(f"Unrecognised route: {self.page.route}")
