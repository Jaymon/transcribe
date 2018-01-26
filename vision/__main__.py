# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import logging
import sys

from captain import exit, echo
from captain.decorators import arg

from vision import __version__, ImagePath, OCR


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(stream=sys.stderr)
log_formatter = logging.Formatter('[%(levelname).1s] %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


@arg("paths", nargs="+", type=ImagePath, default=[], help="path to an image or directory containing images")
@arg("--flow", "--reflow", "-f", action="store_true", help="remove unneccessary newlines in the text")
@arg("--words", "-w", action="store_true", help="print all the words, one on each line")
def main_ocr(paths, flow, words):
    """run every found image through optical Character Recognition to extract the 
    text the image contains

    https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html#text-detection
    """
    for path in paths:
        for image_path in path:
            image = OCR(image_path)
            image.scan()
            if flow:
                echo.out(image.flow)

            elif words:
                for word in image.words:
                    echo.out(word)

            else:
                echo.out(image.text)


def main_safe():
    # https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html#safe-search-detection
    raise NotImplementedError()

exit()

