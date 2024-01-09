from time import sleep

from drybones import FTController

from .models import Page
from .views import ListPagesView, CreatePageView, UpdatePageView


def validate_page(title, text):
    if not title.strip():
        return False, "Title cannot be empty"
    elif not text.strip():
        return False, "Text cannot be empty"
    else:
        return True, ""


class PageController(FTController):
    def index(self):
        pages = Page.all()

        def delete_page(uid):
            page = Page.get(uid)
            page.delete()
            pages.remove(page)
            view.update_state(pages=pages)

        def edit_page(uid):
            self.page.go(f"/page/update/{uid}")

        def create_page():
            self.page.go(f"/page/create")

        view = ListPagesView(delete_page=delete_page, edit_page=edit_page, create_page=create_page)
        self._mount_view(view)
        sleep(2)  # just putting this here to simulate a loading wait - user should see the spinner!
        view.update_state(pages=pages, is_loading=False)

    def create(self):
        def do_validate(title, text):
            validates, msg = validate_page(title, text)
            view.update_state(validates=validates, feedback=msg)

        def do_submit(**payload):
            Page(**payload).upsert()
            self.page.go("/")

        view = CreatePageView(do_validate=do_validate, do_submit=do_submit)
        self._mount_view(view)

    def update(self, uid):
        page = Page.get(uid)

        def do_validate(title, text):
            validates, msg = validate_page(title, text)
            view.update_state(validates=validates, feedback=msg, title=title, text=text)

        def do_submit(**payload):
            payload["page_id"] = uid
            Page(**payload).upsert()
            self.page.go("/")

        view = UpdatePageView(do_validate=do_validate, do_submit=do_submit)
        self._mount_view(view)
        view.update_state(**page.to_dict())
