import logging
import sys
import os

from left import LeftApp
from left.database.tinydbservice import TinyDBService
from .router import on_route_change

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

services = {
     "database": TinyDBService("db.json")
}

LeftApp(
    router_func=on_route_change,
    default_title="Welcome to my app!",
    services=services,
    splash_image=os.path.join(os.getcwd(), r"sampleapp\splash_screen.png"))

