# encoding: utf-8
import os.path

from loguru import logger
from pydub import AudioSegment
from pathlib import Path
from speech_service.config import DATA_DIR
from speech_service.model import AudioInfo, Response
import requests
import shutil
import re
import os
import uuid
import paddle
from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.cli.text.infer import TextExecutor
from datetime import datetime
import math

"""
audio to txt service
"""

MUL_PROCESS = False


def convert_mp3(filename):
    file_path = Path(filename)
    suffix = file_path.suffix
    if not suffix.endswith("mp3"):
        logger.warning("not mp3 suffix, ignore {}", filename)
        return filename
    new_path = file_path.with_suffix(".wav")
    sound = AudioSegment.from_mp3(filename)
    sound.export(str(new_path), format="wav", parameters=["-ac", "1", "-ar", "16000"])
    return str(new_path)


def split(file: str, seconds_per_split_file: int):
    logger.info("split file {}, window length {}", file, seconds_per_split_file)
    if file.split('.')[-1] != 'wav':
        return None
    sound = AudioSegment.from_wav(file)
    seconds_of_file = sound.duration_seconds
    logger.info("file {} duration {}", file, sound.duration_seconds)
    times = math.ceil(int(seconds_of_file) / seconds_per_split_file)
    logger.info("file {} split times {}", file, times)
    start_time = 0
    internal = seconds_per_split_file * 1000
    end_time = seconds_per_split_file * 1000
    name = re.split(r'[\\ .]', file)[-2]
    slice_files = []
    uid = uuid.uuid4().hex
    for i in range(times):
        # 语音文件切割
        part = sound[start_time:end_time]
        data_split_file = (name + "_" + uid + '_' + str(i) + '.wav')
        # 保存切割文件
        part.export(out_f=data_split_file, format="wav")
        start_time += internal
        end_time += internal
        slice_files.append(data_split_file)
    return slice_files


def asr_to_txt(file):
    asr_executor = ASRExecutor()
    text_executor = TextExecutor()
    logger.info("audio to txt {}", file)
    text = asr_executor(
        audio_file=file,
        device=paddle.get_device())
    if text:
        result = text_executor(
            text=text,
            task='punc',
            model='ernie_linear_p3_wudao',
            device=paddle.get_device())
    else:
        result = text
    return result


def audio2txt(filelist):
    # # 并行计算
    # if MUL_PROCESS:
    #     num_cores = int(mp.cpu_count() / 2)
    #     pool = mp.Pool(num_cores)
    #     words = pool.map(asr_to_txt, filelist)
    #     pool.close()
    # else:
    words = []
    for file in filelist:
        result = asr_to_txt(file)
        words.append(result)
    return words


def download_file(url, local_filename):
    start_time = datetime.now()
    if os.path.exists(local_filename):
        logger.warning("file already exists, ignore download url {} , filename {}", url, local_filename)
        return local_filename
    with requests.get(url, stream=False, verify=False, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
            # shutil.copyfileobj(r.raw, f)
    end_time = datetime.now()
    logger.info("download url {} cost {}s", url, (end_time - start_time))


class AudioService(object):

    def __int__(self):
        logger.info("init data dir {}", DATA_DIR)
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)

    def audio_to_txt(self, audio_info: AudioInfo) -> Response:
        if audio_info.file_name is None:
            audio_info.file_name = audio_info.url.split('/')[-1]
        start_time = datetime.now()
        download_file(audio_info.url, audio_info.file_name)
        file = audio_info.file_name
        logger.info("download url done {} file name {}", audio_info.url, audio_info.file_name)
        all_text = self.audio_file_to_txt(file)
        end_time = datetime.now()
        logger.info("{} end audio to text total cost {} s", audio_info.url, (end_time - start_time))
        return Response(200, all_text)

    def audio_file_to_txt(self, file):
        """
        audio file to txt
        :param file:
        :return:
        """
        wav_file = convert_mp3(file)
        file_segments = split(wav_file, 40)
        logger.info("split file {}", file_segments)
        # call seg to txt
        logger.info("start audio to text")
        words = audio2txt(file_segments[0:])
        all_text = "".join(words)
        self.clean_file(file_segments, wav_file)
        return all_text

    def clean_file(self, file_segments, wav_file):
        for file in file_segments:
            os.remove(file)
        if os.path.exists(wav_file):
            os.remove(wav_file)
