from time import sleep

from drybones import FTController
from drybones.helpers import make_props, redirect

from .models import Page
from .views import ListPagesView, CreatePageView, UpdatePageView, ReadPageView
from .actions import go_create_page, go_view_page, go_edit_page, do_validate


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

        props = make_props(go_view_page, go_edit_page, go_create_page, delete_page)
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
        def do_submit(**payload):
            Page(**payload).upsert()
            redirect("/")

        props = make_props(do_validate, do_submit)
        view = CreatePageView(**props)
        self._mount_view(view)

    def update(self, uid):
        page = Page.get(uid)

        def do_submit(**payload):
            payload["page_id"] = uid
            Page(**payload).upsert()
            redirect("/")

        props = make_props(do_validate, do_submit)
        view = UpdatePageView(**props)
        self._mount_view(view)
        view.update_state(**page.to_dict())
