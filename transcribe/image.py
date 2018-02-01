# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
import re

from google.cloud import vision

from .path import Path
from .utils import String


class ImagePath(Path):
    regex = re.compile(r"\.(?:jpe?g|gif|bmp|png|ico|tiff)$", re.I)

    def is_type(self):
        return True if self.regex.search(self) else False


class OCR(object):
    """
    https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html#text-detection
    """
    @property
    def unformatted(self):
        """Return the original text (as it was OCR'd) without any formatting"""
        return String(self._text)

    @property
    def text(self):
        return self.unformatted.flow()

    @property
    def words(self):
        return self._words

    def __init__(self, path):
        self.path = ImagePath(path)
        if not self.path.is_image():
            raise ValueError("{} is not an image path".format(path))

    def scan(self):
        client = vision.Client()
        image = client.image(content=self.path.contents())
        self.response = image.detect_text()

        self._text = ""
        self._words = None
        if self.response:
            self._text = self.response[0].description
            self._words = (w.description for w in self.response[1:])

        return self.response

