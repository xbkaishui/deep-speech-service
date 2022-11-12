from speech_service.service.video_asr import *
from loguru import logger


def test_extract_audio():
    file_name = "/tmp/1.mp4"
    wav_path = extract_audio(file_name)
    logger.info("wav path {}", wav_path)


def test_video_to_txt():
    url = "https://sdinfo-1253622136.cos.ap-shanghai.myqcloud.com/1.mp4"
    video_service = VideoService()
    video_info = VideoInfo(url, "1.mp4", "")
    text = video_service.video_to_txt(video_info)
    logger.info("all text {}", text)