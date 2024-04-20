from functools import cache
from typing import Callable

import flet as ft

from .helpers import get_page


@cache
def loading_spinner(size=50, message=None):
    controls = [ft.ProgressRing(width=size, height=size, stroke_width=2)]
    if message is not None:
        controls.append(ft.Text(message))
    return ft.Row([
            ft.Column(
                controls=controls,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER)


def yes_no_prompt(message: str, title="Please confirm", on_yes: Callable = lambda _: None):
    page = get_page()

    def on_yes_clicked(e):
        on_yes(e)
        page.close_dialog()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.ElevatedButton("Yes", on_click=on_yes_clicked),
            ft.ElevatedButton("No", on_click=lambda _: page.close_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.show_dialog(dlg_modal)
