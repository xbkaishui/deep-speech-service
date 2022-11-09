# encoding: utf-8

from flask import Flask
from loguru import logger
from flask import request
import json
import requests
from speech_service.logging import setup_logging
from speech_service.config import API_PREFIX

app = Flask(__name__)

setup_logging()


@app.route(API_PREFIX + "/")
def hello_world():
    return "<p>hello wechat backend</p>"


@app.route('/sync_audio_to_txt', methods=['POST'])
def sync_audio_to_txt():
    msg = request.get_json()
    logger.info("recv sync_audio_to_txt {}", msg)
    if 'data' not in msg:
        return "init"
