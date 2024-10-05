from typing import Optional, List

import flet as ft


class LeftView:
    @property
    def appbar(self) -> Optional[ft.AppBar]:
        """return how you want the app bar to appear, or None. Called each time the state is updated"""
        return ft.AppBar()

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

    @property
    def bottom_appbar(self) -> Optional[ft.BottomAppBar]:
        return None

    def update_state(self, **new_state):
        """make changes you need to your components whenever the mutable data updates."""
        pass

    def on_view_removed(self):
        """Called when the view is popped from the stack of page.views"""
        pass


class LeftDialog:
    @property
    def title(self) -> ft.Text:
        return ft.Text()

    @property
    def content(self) -> List[ft.Container]:
        return []

    @property
    def actions(self) -> List[ft.Container]:
        return []

    def update_state(self, **new_state):
        """make changes you need to your components whenever the mutable data updates."""
        pass

