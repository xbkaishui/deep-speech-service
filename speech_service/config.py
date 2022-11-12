# encoding: utf-8

import os
from sys import platform

from starlette.config import Config

API_PREFIX = "/api"
VERSION = "1.0"

config = Config("app.env", environ=os.environ)

DEBUG: bool = config("DEBUG", cast=bool, default=False)

LOG_PATH: str = config("LOG_PATH", cast=str, default="logs")

DATA_DIR = config("DATA_DIR", cast=str, default="data")

MAX_CPU = config("MAX_CPU", cast=int, default=8)

if platform == "darwin":
    ...
