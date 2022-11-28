# encoding: utf-8

from loguru import logger
from flask import Flask, jsonify
from flask import request
from speech_service.logging import setup_logging
from speech_service.config import API_PREFIX
from .service.audio_asr import AudioService
from .service.video_asr import VideoService
from .model import AudioInfo, VideoInfo
from .remote_actor import RemoteSpeechActor
# from pathos.pools import ProcessPool as Pool
from pathos.pools import ThreadPool as Pool
from .config import MAX_CPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

setup_logging()
pool = Pool(nodes=MAX_CPU)


@app.route(API_PREFIX + "/")
def index():
    return "<p>hello speech service</p>"


@app.route(API_PREFIX + '/audio_to_txt', methods=['POST'])
def audio_to_txt():
    msg = request.get_json()
    logger.info("recv audio_to_txt {}", msg)
    url = msg["url"]
    file_name = msg["file_name"]
    audio_service = AudioService()
    resp = audio_service.audio_to_txt(AudioInfo(url, file_name))
    return jsonify({"code": resp.code, "data": resp.data})


@app.route(API_PREFIX + '/video_to_txt', methods=['POST'])
def video_to_txt():
    msg = request.get_json()
    logger.info("recv video_to_txt {}", msg)
    url = msg["url"]
    file_name = msg["file_name"]
    video_service = VideoService()
    resp = video_service.video_to_txt(VideoInfo(url, file_name))
    return jsonify({"code": resp.code, "data": resp.data})


@app.route(API_PREFIX + '/video_to_timeline', methods=['POST'])
def video_to_timeline():
    msg = request.get_json()
    logger.info("recv video_to_txt {}", msg)
    url = msg["url"]
    file_name = msg["file_name"]
    video_service = VideoService()
    resp = video_service.video_to_timeline(VideoInfo(url, file_name))
    return jsonify({"code": resp.code, "data": resp.data})


@app.route(API_PREFIX + '/async_audio_to_txt', methods=['POST'])
def async_audio_to_txt():
    msg = request.get_json()
    logger.info("recv async_audio_to_txt {}", msg)
    if 'callback_url' not in msg:
        raise Exception("async should provide callback_url")
    actor = RemoteSpeechActor()
    pool.amap(actor.audio_to_txt, [msg])
    return jsonify({"code": 200, "data": ""})


@app.route(API_PREFIX + '/async_video_to_txt', methods=['POST'])
def async_video_to_txt():
    msg = request.get_json()
    logger.info("recv async_video_to_txt {}", msg)
    if 'callback_url' not in msg:
        raise Exception("async should provide callback_url")
    actor = RemoteSpeechActor()
    pool.amap(actor.video_to_txt, [msg])
    return jsonify({"code": 200, "data": ""})


@app.route(API_PREFIX + '/callback', methods=['POST'])
def callback():
    msg = request.get_json()
    logger.info("recv callback {}", msg)
    return "ok"


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
    logger.error(str(e), e)
    return jsonify(data)

