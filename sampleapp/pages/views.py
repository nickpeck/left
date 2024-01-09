import flet as ft

from drybones.view import FTView
from drybones.sharedcomponents import loading_spinner


class PageBaseView(FTView):
    @property
    def appbar(self):
        return ft.AppBar(
            title=ft.Text(self.title),
            actions=[])


class ListPagesView(PageBaseView):
    def __init__(self, delete_page, edit_page, create_page, view_page):
        self.delete_page = delete_page
        self.edit_page = edit_page
        self.create_page = create_page
        self.view_page = view_page
        self.state = {"is_loading": True, "pages": []}

    @property
    def title(self):
        return "List Pages"

    @property
    def appbar(self):
        bar = super().appbar
        bar.automatically_imply_leading = False
        bar.leading = None
        return bar

    def update_state(self, **new_state):
        self.state.update(new_state)

    def make_page_card(self, page):
        def delete_prompt(e):
            def close_and_delete(x):
                x.page.close_dialog()
                self.delete_page(page.key)

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to delete this page?"),
                actions=[
                    ft.ElevatedButton("Yes", on_click=close_and_delete),
                    ft.ElevatedButton("No", on_click=lambda x: x.page.close_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            e.page.show_dialog(dlg_modal)

        return ft.Card(
            content=ft.Column([
                ft.Text(page.title),
                ft.Text(page.short_text),
                ft.Row([
                    ft.IconButton(ft.icons.DELETE,
                                  on_click=delete_prompt),
                    ft.IconButton(ft.icons.EDIT,
                                  on_click=lambda e: self.edit_page(page.key)),
                    ft.IconButton(ft.icons.PLAY_ARROW,
                                  on_click=lambda e: self.view_page(page.key))
                ])
            ])
        )

    @property
    def controls(self):
        if self.state.get("is_loading", False):
            return [loading_spinner(size=50)]
        controls = [ft.ElevatedButton("Create a page", on_click=lambda e: self.create_page())]
        for page in self.state.get("pages", []):
            controls.append(self.make_page_card(page))
        return controls


class CreatePageView(PageBaseView):
    def __init__(self, do_validate, do_submit):
        self.state = {"title": "", "text": "", "validates": False, "feedback": None}
        self.feedback = ft.Text("", color=ft.colors.RED)
        self.title_input = ft.TextField(label="The title",
                                        on_blur=lambda e: do_validate(
                                            title=self.title_input.value, text=self.text_input.value))
        self.text_input = ft.TextField(label="The title",
                                       multiline=True,
                                       height=200,
                                       min_lines=10,
                                       on_blur=lambda e: do_validate(
                                            title=self.title_input.value, text=self.text_input.value))
        self.submit = ft.ElevatedButton("Submit", disabled=True,
                                        on_click=lambda e: do_submit(
                                            title=self.title_input.value, text=self.text_input.value))
        self.update_state()

    @property
    def title(self):
        return "Create a page"

    def update_state(self, **new_state):
        self.state.update(new_state)
        self.feedback.value = self.state["feedback"] if not self.state["validates"] else ""
        self.submit.disabled = not self.state["validates"]

    @property
    def controls(self):
        return [
            self.feedback,
            self.title_input,
            self.text_input,
            self.submit
        ]


class UpdatePageView(CreatePageView):
    @property
    def title(self):
        return "Update a page"

    def update_state(self, **new_state):
        self.state.update(new_state)
        self.title_input.value = self.state["title"]
        self.text_input.value = self.state["text"]
        self.feedback.value = self.state["feedback"] if not self.state["validates"] else ""
        self.submit.disabled = not self.state["validates"]


class ReadPageView(PageBaseView):

    def __init__(self):
        self.state = {"title": "", "text": ""}
        self.text_view = ft.Text()

    @property
    def title(self):
        return self.state["title"]

    def update_state(self, **new_state):
        self.state.update(new_state)
        self.text_view.value = self.state["text"]

    @property
    def controls(self):
        return [
            self.text_view
        ]
