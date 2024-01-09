from functools import cache

import flet as ft


@cache
def loading_spinner(size=50):
    return ft.Row([
            ft.Column(
                [
                    ft.ProgressRing(width=size, height=size, stroke_width=2)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER)
