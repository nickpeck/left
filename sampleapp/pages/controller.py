from time import sleep

from drybones import FTController
from drybones.helpers import make_props

from .models import Page
from .views import ListPagesView, CreatePageView, UpdatePageView, ReadPageView


def validate_page(title, text):
    if not title.strip():
        return False, "Title cannot be empty"
    elif not text.strip():
        return False, "Text cannot be empty"
    else:
        return True, ""

class PageController(FTController):
    def index(self):
        has_visited = self.page.session.get("has_visited")
        if not has_visited:
            self.page.session.set("has_visited", True)
        pages = Page.all()

        def delete_page(uid):
            page = Page.get(uid)
            page.delete()
            pages.remove(page)
            view.update_state(pages=pages)

        def edit_page(uid):
            self.page.go(f"/page/update/{uid}")

        def view_page(uid):
            self.page.go(f"/page/view/{uid}")

        def create_page():
            self.page.go(f"/page/create")

        props = make_props(locals(), "create_page", "edit_page", "delete_page", "view_page")

        view = ListPagesView(**props)
        self._mount_view(view)
        if not has_visited:
            sleep(2)  # just putting this here to simulate a little loading wait - user should see the spinner!
        view.update_state(pages=pages, is_loading=False)

    def view(self, uid):
        page = Page.get(uid)
        view = ReadPageView()
        self._mount_view(view)
        view.update_state(**page.to_dict())

    def create(self):
        def do_validate(title, text):
            validates, msg = validate_page(title, text)
            view.update_state(validates=validates, feedback=msg)

        def do_submit(**payload):
            Page(**payload).upsert()
            self.page.go("/")

        props = make_props(locals(), "do_validate", "do_submit")
        view = CreatePageView(**props)
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

        props = make_props(locals(), "do_validate", "do_submit")
        view = UpdatePageView(**props)
        self._mount_view(view)
        view.update_state(**page.to_dict())
