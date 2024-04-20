"""
Entry point when using 'flet build web' to create a front end web app with Pyodide.
See database/restapiservice.py for integration w. back-end API.
"""

import logging
import sys

import flet as ft

from left import LeftApp
from left.database.restapiservice import RESTfulService
from router import on_route_change


async def main(page):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    services = {
        "database": RESTfulService("/api/v1")
    }
    await LeftApp(router_func=on_route_change, default_title="Welcome to my app!", services=services)(page)


ft.app(main)
