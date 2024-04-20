import flet as ft

from left.view import LeftView
from left.sharedcomponents import loading_spinner


class PageBaseView(LeftView):
    @property
    def appbar(self):
        return ft.AppBar(title=ft.Text(self.title), actions=[])


class ListPagesView(PageBaseView):
    def __init__(self, delete_page, go_edit_page, go_create_page, go_view_page):
        self.delete_page = delete_page
        self.go_edit_page = go_edit_page
        self.go_create_page = go_create_page
        self.go_view_page = go_view_page
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
        async def prompt_and_delete(e):
            async def delete_and_close(x):
                await self.delete_page(page.key)
                await x.page.close_dialog_async()

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to delete this page?"),
                actions=[
                    ft.ElevatedButton("Yes", on_click=delete_and_close),
                    ft.ElevatedButton("No", on_click=lambda x: x.page.close_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            await e.page.show_dialog_async(dlg_modal)

        return ft.Card(
            content=ft.Column([
                ft.Text(page.title),
                ft.Text(page.short_text),
                ft.Row([
                    ft.IconButton(ft.icons.DELETE,
                                  on_click=prompt_and_delete),
                    ft.IconButton(ft.icons.EDIT,
                                  on_click=self.go_edit_page(page.key)),
                    ft.IconButton(ft.icons.PLAY_ARROW,
                                  on_click=self.go_view_page(page.key))
                ])
            ])
        )

    @property
    def controls(self):
        if self.state.get("is_loading", False):
            return [loading_spinner(size=50)]
        controls = [ft.ElevatedButton("Create a page", on_click=self.go_create_page)]
        for page in self.state.get("pages", []):
            controls.append(self.make_page_card(page))
        return controls


class CreatePageView(PageBaseView):
    def __init__(self, do_validate, do_submit):
        self.state = {"title": "", "text": "", "validates": False, "feedback": None}
        self.feedback = ft.Text("", color=ft.colors.RED)
        self.title_input = ft.TextField(label="The title")
        self.text_input = ft.TextField(label="The title",
                                       multiline=True,
                                       height=200,
                                       min_lines=10)
        self.text_input.on_blur = do_validate(
                                            self,
                                            title_input=self.title_input, text_input=self.text_input)

        self.title_input.on_blur = do_validate(
                                            self,
                                            title_input=self.title_input, text_input=self.text_input)
        self.submit = ft.ElevatedButton("Submit", disabled=True)
        self.submit.on_click = do_submit(title_input=self.title_input, text_input=self.text_input)
        self.update_state()

    @property
    def title(self):
        return "Create a page"

    def update_state(self, **new_state):
        self.state.update(new_state)
        validates = self.state.get("validates", False)
        self.feedback.value = self.state.get("feedback", "") if not validates else ""
        self.submit.disabled = not validates

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
        self.title_input.value = self.state.get("title", "")
        self.text_input.value = self.state.get("text", "")
        validates = self.state.get("validates", False)
        self.feedback.value = self.state.get("feedback", "") if not validates else ""
        self.submit.disabled = not validates


class ReadPageView(PageBaseView):

    def __init__(self):
        self.state = {"title": "", "text": ""}
        self.text_view = ft.Text()

    @property
    def title(self):
        return self.state.get("title", "")

    def update_state(self, **new_state):
        self.state.update(new_state)
        self.text_view.value = self.state.get("text", "")

    @property
    def controls(self):
        return [
            self.text_view
        ]
