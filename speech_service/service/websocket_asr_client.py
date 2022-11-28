import asyncio
import os

from loguru import logger
from paddlespeech.server.utils.audio_handler import ASRWsAudioHandler
from datetime import datetime


def asr_client(server_ip: str = '127.0.0.1', port: int = 8090,
               punc_server_ip: str = '127.0.0.1', punc_server_port: int = 8190,
               endpoint: str = "/paddlespeech/asr/streaming", wavfile: str = None):
    start_time = datetime.now()
    logger.info("asr websocket client start")
    handler = ASRWsAudioHandler(
        server_ip,
        port,
        endpoint=endpoint,
        punc_server_ip=punc_server_ip,
        punc_server_port=punc_server_port)
    loop = asyncio.get_event_loop()
    result = {}
    # support to process single audio file
    if wavfile and os.path.exists(wavfile):
        logger.info(f"start to process the wavscp: {wavfile}")
        result = loop.run_until_complete(handler.run(wavfile))
        logger.info(f"result type {type(result)}")
        # logger.info(f"asr websocket client finished : {result}")
    end_time = datetime.now()
    logger.info("asr_client convert {} cost {}s", wavfile, (end_time - start_time))
    return result


if __name__ == "__main__":
    logger.info("Start to do streaming asr client")
    res = asr_client(wavfile="/tmp/1_vd_8c2236ac046441f89f9e4b9727bfcb57_0.wav")
    logger.info(f"End to do streaming {res}")
