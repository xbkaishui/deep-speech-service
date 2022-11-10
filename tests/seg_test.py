from pydub import AudioSegment
import logging


def test_seg():
    l = logging.getLogger("pydub.converter")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    podcast = AudioSegment.from_mp3("12.mp3")
    podcast.export("12.wav", format="wav", parameters=["-ac", "1", "-ar", "16000"])


if __name__ == '__main__':
    test_seg()