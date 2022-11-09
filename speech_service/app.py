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
def index():
    return "<p>hello speech service</p>"


@app.route(API_PREFIX + '/audio_to_txt', methods=['POST'])
def audio_to_txt():
    msg = request.get_json()
    logger.info("recv audio_to_txt {}", msg)
    ...


@app.route(API_PREFIX + '/async_audio_to_txt', methods=['POST'])
def async_audio_to_txt():
    msg = request.get_json()
    logger.info("recv async_audio_to_txt {}", msg)
    ...


@app.route(API_PREFIX + '/async_video_to_txt', methods=['POST'])
def async_video_to_txt():
    msg = request.get_json()
    logger.info("recv async_video_to_txt {}", msg)
    ...

