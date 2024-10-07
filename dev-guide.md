# Developer Guide

## App Entry Point

The entry point is typically named main.py, in the root of the project directory.

At a minimum, you will need to create an instance of class LeftApp:

```python
from left import LeftApp

LeftApp(default_title="App Title")
```

If the app requires any kind of persistent data storage, you will probably need some kind of database.
This is defined as a 'service'. Left contains a wrapper around Tinybd/TinyRecord that is suitable for apps that 
deal with small data sets stored in a local json file (such as a user's app configuration settings). 

This allows us to configure a storage backend independent of the data Model implementation (see below). In theory,
other database or API implementations could be built that extend left.database.documentrecordservice.DocumentRecordService.

```python
from left import LeftApp
from left.database.tinydbservice import TinyDBService

services = {
     "database": TinyDBService("db.json")
}

LeftApp(
    default_title="App Title",
    services=services)
```

The app instance is a singleton that can be accessed where required using the .get_app() method.
The database service will now be accessible throughout the app using ```LeftApp.get_app().services["database"]```

## Data Models

You can define classes to model your data, if required. (Left does not include an ORM), but this example should suffice
for simple document-style storage.

Here, we define a dataclass to represent a page record.

```python
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

from left.model import LeftModel

@dataclass_json
@dataclass
class Page(LeftModel):
    __pk__ = "page_id"
    title: str = ""
    text: str = ""
    page_id: Optional[str] = None
```

If using the DocumentRecordService, the class should define a class attribute `__pk__` that identifies the name of the
attribute that will be used as the document key for query purposes (in this case, Page.page_id)

## Controllers

Controller classes should extend LeftController. Here we define two possible actions for listing pages, and displaying
a single page:

```python
from left import LeftController

class PageController(LeftController):
    def index(self):
        pages = Page.all()

    def view_page(self):
        
```

At the moment, this controller will not render anything, so we need to define a view to hold our presentation layer
## Views

Views should extend LeftView. Here, we use a state attribute to represent the mutable data passed in from the Controller:

```python
import flet as ft
from left.view import LeftView

class PageView(LeftView):
    def __init__(self):
        self.state = {"page": None}

    @property
    def controls(self):
        if self.state["page"] is None:
            return [ft.Text("loading...")]
        return [
            ft.Text(self.state["page"].get("title", "")),
            ft.Text(self.state["page"].get("text", ""))
        ]

```

A LeftView contains properties that return flet controls for different areas of a flet view: appbar, controls, drawer, 
end_drawer, bottom_appbar.

Because we are dealing with SPA-like applications, the view is mounted on top of the page inside the controller when we
use the _mount_view() method:

```python
from left import LeftController

class PageController(LeftController):
    
    def view(self, page_id):
        view = PageView()
        self._mount_view(view, layered=True)
        page = Page.get(page_id)
        view.update_state(**page.to_dict())
```
Once the view is mounted to the page, whenever we call view.update_state, it will automatically cause the page
to refresh.

In the example above, this allowed us to render the view with a 'loading...' message whilst we retrieved the page
record. We then called view.update_state() with the retrieved record which would then be displayed using the controls
defined in Pageview.controls.


## Routing

Before we can run the app, it will require a router function that defines one or more views. This is supplied to the top level LeftApp constructor:

```python
from left import LeftApp

services = ...

def on_route_changed(page, parts):
    match parts:
        case ['']:
            PageController(page).index()
        case ['page', 'view', uid]:
            PageController(page).view(uid)
        case _:
            print(f"Unrecognised route: {page.route}")

LeftApp(
    default_title="App Title",
    on_route_changed=on_route_changed,
    services=services)
```

You should now be able to run the app. You can either invoke main.py directly, or use one of the flet commands to control
whether to run as a web or native app:

```commandline
flet run -w -r -p 8080 # run as a web app, with reloading on port 8080
flet run -r # run as a native app
```

## Interactions

Typically, we would want to define action callbacks outside of the view layer. For example, to define a page delete action:

```python
from left.helpers import make_props, redirect

# might want to define actions outside of the controller if they might be shared between controllers?
def go_delete_page(page_id):
    p = Page.get(page_id)
    p.delete()
    redirect("/") # use redirect to perform route changes

class PageController(LeftController):
    
    def view(self, page_id):                    
        view = PageView(**make_props(go_delete_page))
        self._mount_view(view, layered=True)
        page = Page.get(page_id)
        view.update_state(**page.to_dict())


class PageView(LeftView):
    def __init__(self, go_delete_page):
        self.go_delete_page = go_delete_page
        self.state = {"page": None}

    @property
    def controls(self):
        if self.state["page"] is None:
            return [ft.Text("loading...")]
        return [
            ...
            ft.Button("Delete Page?", 
                      on_click=lambda _: self.go_delete_page(self.state["page"].get("page_id", "")))
        ]
```

## Pre-Startup Hook

Sometimes, you may want to run some actions before the app starts acting on the routing changes. LeftApp allows you to
provide a pre_startup_hook for this purpose. Typically, you might want to use this to ensure that a 'settings' entry
is saved on the first run:

```python
class Settings(LeftModel):
    ...

def pre_startup(app: LeftApp):
    """If no settings, assume first run, and prompt for root media folder"""
    try:
        settings = Settings.get_settings()
    except SettingsNotFound:
        settings = Settings()
        settings.upsert()
    app.opts["default_title"] = settings.site_name

LeftApp(
    pre_startup_hook=pre_startup,
    ...)
```
    
## Creating Addon Modules

You can build an app that has facility for addon (or plugin) modules that might be shipped at a later stage.

These should live in a location supplied to the app by the environment variable `LEFT_ADDON_PATH` (default folder 'addons' adjacent to the execution
directory). Each addon module can define an 'on_load' hook at the module root that will receive the main app instance, as
well as an 'on_route_changed' function, that will be executed after the main app's router function.

```python
# addons/myaddonmodule/__init__.py
def on_load(_app: LeftApp):
    # any actions to be taken on load, ie storing settings in the db
    pass

def on_route_changed(page, parts):
    # act on any routes specific to this addonn
    pass

```