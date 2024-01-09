import logging
import sys

from drybones import FTApp
from drybones.database.tinydbservice import TinyDBService
from .router import MyRouter

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

FTApp(router_cls=MyRouter, default_title="Welcome to my app!", services=services)
