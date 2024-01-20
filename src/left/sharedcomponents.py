from functools import cache

import flet as ft


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
