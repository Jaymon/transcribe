# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import logging
import sys

from captain import exit as console, echo
from captain.decorators import arg

from transcribe import __version__
from transcribe.path import Paths
from transcribe.image import ImagePath, OCR
from transcribe.speech import SpeechPath, Speech
from transcribe.utils import Time


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(stream=sys.stderr)
log_formatter = logging.Formatter('[%(levelname).1s] %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


@arg("paths", nargs="+", default=[], help="path to an image or directory containing images")
@arg("--no-flow",
     dest="noflow",
     action="store_true",
     help="text will not be reformatted to remove unnecessary newlines",
)
@arg("--words", "-w", action="store_true", help="print all the words, one on each line")
def main_ocr(paths, noflow, words):
    """run every found image through optical Character Recognition to extract the 
    text the image contains

    https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html#text-detection
    """
    paths = Paths(paths, ImagePath)
    for path in paths:
        f = OCR(path)
        f.scan()
        if words:
            for word in f.words:
                echo.out(word)

        elif noflow:
            echo.out(f.unformatted)

        else:
            echo.out(f.text)


@arg("paths", nargs="+", default=[], help="path to a sound file or directory containing audio files")
@arg("--start", type=Time, default=0, help="transcribe from this time forward (format HH:MM:SS)")
@arg("--stop", type=Time, default=0, help="transcribe to this time (format HH:MM:SS)")
@arg("--language", "--lang", dest="lang", default='en-US', help="The spoken language of the audio file(s)")
def main_speech(paths, start, stop, lang):
    """Create a transcript of each audio file"""
    paths = Paths(paths, SpeechPath)
    for path in paths:
        f = Speech(path, lang)
        f.scan(start, stop)

        for time, text in f:
            echo.out("{:<15}{}", time, text)


console(__name__)

