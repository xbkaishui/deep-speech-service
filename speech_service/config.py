import os
from sys import platform

from starlette.config import Config

API_PREFIX = "/api"
VERSION = "1.0"

config = Config("app.env", environ=os.environ)

DEBUG: bool = config("DEBUG", cast=bool, default=False)

LOG_PATH: str = config("LOG_PATH", cast=str, default="logs")

if platform == "darwin":
    ...
