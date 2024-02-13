from time import sleep

from left import LeftController
from left.helpers import make_props, redirect

from .models import Page
from .views import ListPagesView, CreatePageView, UpdatePageView, ReadPageView
from .actions import go_create_page, go_view_page, go_edit_page, do_validate


class PageController(LeftController):
    async def index(self):
        has_visited = self.page.session.get("has_visited")
        if not has_visited:
            self.page.session.set("has_visited", True)
        pages = Page.all()

        async def delete_page(uid):
            page = Page.get(uid)
            page.delete()
            pages.remove(page)
            await view.update_state(pages=pages)

        props = make_props(go_view_page, go_edit_page, go_create_page, delete_page)
        view = ListPagesView(**props)
        await self._mount_view(view)
        if not has_visited:
            sleep(2)  # just putting this here to simulate a little loading wait - user should see the spinner!
        await view.update_state(pages=pages, is_loading=False)

    async def view(self, uid):
        page = Page.get(uid)
        view = ReadPageView()
        await self._mount_view(view, layered=True)
        await view.update_state(**page.to_dict())

    async def create(self):
        def do_submit(title_input, text_input):
            async def f(_):
                Page(title=title_input.value, text=text_input.value).upsert()
                await redirect("/")
            return f

        props = make_props(do_validate, do_submit)
        view = CreatePageView(**props)
        await self._mount_view(view, layered=True)

    async def update(self, uid):
        page = Page.get(uid)

        def do_submit(title_input, text_input):
            async def f(_):
                Page(page_id=uid, title=title_input.value, text=text_input.value).upsert()
                await redirect("/")
            return f

        props = make_props(do_validate, do_submit)
        view = UpdatePageView(**props)
        await self._mount_view(view, layered=True)
        await view.update_state(**page.to_dict())
