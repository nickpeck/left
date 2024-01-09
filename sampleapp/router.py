from typing import List

from drybones import FTRouter

from .pages.controller import PageController


class MyRouter(FTRouter):
    def on_route_change(self, parts: List[str]):
        match parts:
            case ['']:
                PageController(self.page).index()
            case ['page', 'create']:
                PageController(self.page).create()
            case ['page', 'update', uid]:
                PageController(self.page).update(uid)
            case ['page', 'delete', uid]:
                PageController(self.page).delete(uid)
            case _:
                print(f"Unrecognised route: {self.page.route}")
