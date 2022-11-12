# encoding: utf-8
from pathlib import Path

from loguru import logger
import moviepy.editor as mp
from speech_service.model import VideoInfo, Response
import os
import warnings

from speech_service.service.audio_asr import download_file, AudioService

warnings.filterwarnings('ignore')


"""
video to txt service
"""


def extract_audio(videos_file_path):
    my_clip = mp.VideoFileClip(videos_file_path, audio_fps=16000)
    path = Path(videos_file_path)
    if path.suffix.endswith("mp4"):
        new_file_name = path.stem + "_vd.wav"
        my_clip.audio.write_audiofile(new_file_name)
    else:
        raise Exception("not format mp4")
    return new_file_name


class VideoService(object):

    def video_to_txt(self, video_info: VideoInfo) -> Response:
        if video_info.file_name is None:
            video_info.file_name = video_info.url.split('/')[-1]
        download_file(video_info.url, video_info.file_name)
        file = video_info.file_name
        logger.info("download url done {} file name {}", video_info.url, video_info.file_name)
        wav_file = extract_audio(file)
        audio_service = AudioService()
        all_text = audio_service.audio_file_to_txt(wav_file)
        return Response(200, all_text)