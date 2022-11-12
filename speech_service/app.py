# encoding: utf-8

from flask import Flask, jsonify
from loguru import logger
from flask import request
from speech_service.logging import setup_logging
from speech_service.config import API_PREFIX
from .service.audio_asr import AudioService
from .service.video_asr import VideoService
from .model import AudioInfo, VideoInfo

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

setup_logging()

audioService = AudioService()
videoService = VideoService()


@app.route(API_PREFIX + "/")
def index():
    return "<p>hello speech service</p>"


@app.route(API_PREFIX + '/audio_to_txt', methods=['POST'])
def audio_to_txt():
    msg = request.get_json()
    logger.info("recv audio_to_txt {}", msg)
    url = msg["url"]
    file_name = msg["file_name"]
    resp = audioService.audio_to_txt(AudioInfo(url, file_name))
    return jsonify({"code": resp.code, "data": resp.data})


@app.route(API_PREFIX + '/video_to_txt', methods=['POST'])
def video_to_txt():
    msg = request.get_json()
    logger.info("recv video_to_txt {}", msg)
    url = msg["url"]
    file_name = msg["file_name"]
    resp = videoService.video_to_txt(VideoInfo(url, file_name))
    return jsonify({"code": resp.code, "data": resp.data})


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


@app.errorhandler(Exception)
def error_handler(e):
    """
    global exception handler
    :param e:
    :return:
    """
    data = {
        "code": -1,
        "msg": str(e),
        "data": None
    }
    return jsonify(data)