from speech_service.service.audio_asr import *
from loguru import logger


def test_convert_mp3():
    file_name = "../12.mp3"
    wav_path = convert_mp3(file_name)
    logger.info("wav path {}", wav_path)


def test_split():
    file_name = "/tmp/202210171520035574.mp3"
    wav_file = convert_mp3(file_name)
    split_files = split(wav_file, 40)
    logger.info("split files {}", split_files)


def test_audio2txt():
    file = "_0.wav"
    words = audio2txt([file])
    all_text = ''.join(words)
    logger.info("all text {}", all_text)


def test_download_file():
    url = "https://qywechat-1257844667.cos.ap-shanghai.myqcloud.com/20221108/202211081344184076.mp3"
    download_file(url, "/tmp/test.mp3")