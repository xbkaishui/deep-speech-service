from loguru import logger
import requests
# import ray
from .service.audio_asr import AudioService
from .service.video_asr import VideoService
from .model import AudioInfo, VideoInfo


headers = {
    'Content-Type': 'application/json'
}



# @ray.remote
class RemoteSpeechActor(object):

    def audio_to_txt(self, msg: dict):
        audio_info = AudioInfo(msg["url"], msg["file_name"], msg["callback_url"])
        logger.info("recv async audio to txt {}", audio_info)
        audio_service = AudioService()
        resp = audio_service.audio_to_txt(audio_info)
        response = requests.request("POST", audio_info.callback_url, headers=headers, data=resp.to_json())
        logger.info("send req {} resp {}", resp.to_json(), response)

    def video_to_txt(self, msg: dict):
        video_info = VideoInfo(msg["url"], msg["file_name"], msg["callback_url"])
        logger.info("recv async video to txt {}", video_info)
        video_service = VideoService()
        resp = video_service.video_to_txt(video_info)
        response = requests.request("POST", video_info.callback_url, headers=headers, data=resp.to_json())
        logger.info("send req {} resp {}", resp.to_json(), response)