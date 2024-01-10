"""Some small functions we can share between controller methods"""
from left.view import FTView
from left.helpers import redirect


def validate_page(title, text):
    """Basic validator, but could use schema-based validation, or pydantic..."""
    if not title.strip():
        return False, "Title cannot be empty"
    elif not text.strip():
        return False, "Text cannot be empty"
    else:
        return True, ""


def do_validate(view: FTView, **kwargs):
    """Validate, and update the view with the result"""
    validates, msg = validate_page(
        title=kwargs.get("title", ""),
        text=kwargs.get("text", ""))
    kwargs.update({
        "validates": validates,
        "feedback": msg
    })
    view.update_state(**kwargs)


def go_edit_page(uid: str):
    redirect(f"/page/update/{uid}")


def go_view_page(uid: str):
    redirect(f"/page/view/{uid}")


def go_create_page():
    redirect(f"/page/create")
