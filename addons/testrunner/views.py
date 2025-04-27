from left import LeftView
import flet as ft


class ResultsView(LeftView):

    def __init__(self):
        self.state = {'results': []}

    @property
    def controls(self):
        return [
            ft.Column(
                controls=[ft.Row(
                    controls=[
                        ft.Text(result)
                    ]
                ) for result in self.state['results']]
            )
        ]
