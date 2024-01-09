from typing import Optional, List

import flet as ft


class FTView:
    @property
    def appbar(self) -> Optional[ft.AppBar]:
        """return how you want the app bar to appear, or None. Called each time the state is updated"""
        return ft.AppBar([ft.Text("The Page Title")])

    @property
    def controls(self) -> List[ft.Container]:
        """use this to define how your main body components are arranged. Called each time after the state is updated"""
        return []

    @property
    def drawer(self) -> Optional[ft.NavigationDrawer]:
        return None

    @property
    def end_drawer(self):
        return None

    @property
    def floating_action_button(self) -> Optional[ft.FloatingActionButton]:
        return None

    def update_state(self, **new_state):
        """make changes you need to your components whenever the mutable data updates."""
        pass