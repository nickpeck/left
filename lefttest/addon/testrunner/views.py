from typing import List
from lefttest.testresult import TestResult

from left import LeftView
from left.helpers import get_page
import flet as ft


class ResultsView(LeftView):

    def __init__(self):
        self.state = {'results': {}}

    @property
    def controls(self):
        return [
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Text(testclass),
                    self._create_testclass_summary(results)]))
            for testclass, results in self.state['results'].items()
        ]

    @staticmethod
    def _create_testclass_summary(results: List[TestResult]) -> ft.DataTable:
        return ft.DataTable(
            width=get_page().width,
            columns=[
                ft.DataColumn(ft.Text("test name")),
                ft.DataColumn(ft.Text("passed")),
                ft.DataColumn(ft.Text("traceback"))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(r.test_name)),
                    ft.DataCell(ft.ElevatedButton(r.passed, color=ft.Colors.GREEN if r.passed else ft.Colors.RED)),
                    ft.DataCell(ft.Text(r.stacktrace))
                ]) for r in results
            ],
            expand=True
        )
