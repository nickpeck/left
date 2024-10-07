# LEFT, a Minimalist Flet Framework

A very simple framework using the flet library - the bare boilerplate code I use to get some apps up and running.

I have deliberately kept things extremely simple - it doesn't attempt to hide the flet internals,
 very little enforced convention/configuration, and only a tiny reliance on some 'magic' in 
 the React-influenced state management in the view layer (even this is not mandatory).

Its up to the end user to organise their implementation in a consistent and logical manner that works for them.

dev usage (requires python >= 3.10)

~~~commandline
pip install python-left
~~~

See [Developer Guide](dev-guide.md) and sampleapp/ for a more fully-fledged CRUD-app example.

Here is the simplest possible app usage:

```python
import flet as ft
from left import LeftApp, LeftController, LeftView
from left.sharedcomponents import loading_spinner
from left.helpers import redirect


class MyView(LeftView):
    def __init__(self):
        self.state = {"message": None}

    def update_state(self, **new_state):
        self.state.update(new_state)

    @property
    def appbar(self):
        return ft.AppBar(
            actions=[
                ft.ElevatedButton("Home", on_click=lambda _: redirect("/")),
                ft.ElevatedButton("Page2", on_click=lambda _: redirect("/page/view/page2"))
            ]
        )

    @property
    def controls(self):
        if self.state["message"] is None:
            return [loading_spinner()]
        return [
            ft.Text(self.state["message"])
        ]


class MyController(LeftController):
    def index(self):
        view = MyView()
        self._mount_view(view)
        view.update_state(message="welcome to the app!")

    def load_page(self, uid):
        view = MyView()
        self._mount_view(view)
        view.update_state(message=f"Display contents for {uid} here...")


def on_route_change(page, parts):
    match parts:
        case ['']:
            MyController(page).index()
        case ['page', 'view', uid]:
            MyController(page).load_page(uid)
        case _:
            print(f"Unrecognised route: {page.route}")


LeftApp(
    router_func=on_route_change,
    default_title="A Very Simple App")

```