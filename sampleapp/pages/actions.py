"""Some small functions we can share between controller methods"""
from left.view import LeftView
from left.helpers import redirect

import flet as ft


def validate_page(title, text):
    """Basic validator, but could use schema-based validation, or pydantic..."""
    if not title.strip():
        return False, "Title cannot be empty"
    elif not text.strip():
        return False, "Text cannot be empty"
    else:
        return True, ""


def do_validate(view: LeftView, title_input: ft.TextField, text_input: ft.TextField):
    """Validate, and update the view with the result"""
    async def f(_):
        validates, msg = validate_page(
            title=title_input.value,
            text=text_input.value)
        response = {
            "validates": validates,
            "feedback": msg,
            "title": title_input.value,
            "text": text_input.value
        }
        await view.update_state(**response)
    return f


def go_edit_page(uid: str):
    async def f(_):
        await redirect(f"/page/update/{uid}")
    return f


def go_view_page(uid: str):
    async def f(_):
        await redirect(f"/page/view/{uid}")
    return f


async def go_create_page(_):
    await redirect("/page/create")
