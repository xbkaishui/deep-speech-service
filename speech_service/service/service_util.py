from loguru import logger
import re


def parse_timeline(asr_result: dict, offset=0.0):
    segment = asr_result['result']
    times = asr_result['times']
    sentences = re.split("？|，|。", segment, 100)
    timelines = []
    word_cnt = 0
    for sentence in sentences:
        # logger.info("sentence {}", sentence)
        if len(sentence.strip()) == 0:
            continue
        sentence_cnt = len(sentence)
        start_word_idx = word_cnt
        end_word_idx = start_word_idx + sentence_cnt -1
        start_word = times[start_word_idx]
        end_word = times[end_word_idx]
        logger.info(f'start_idx {start_word_idx} start word {start_word["w"]}, end_idx {end_word_idx} end word {end_word["w"]}')
        word_cnt = word_cnt + sentence_cnt
        timeline = {"sentence": sentence, "bg": start_word["bg"] + offset, "ed": end_word["ed"] + offset}
        timelines.append(timeline)
        # logger.info(f"timeline {timeline}")
    return timelines
