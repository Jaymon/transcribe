# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
import re

from google.cloud import vision

from .path import Path


class ImagePath(Path):
    regex = re.compile(r"\.(?:jpe?g|gif|bmp|png|ico|tiff)$", re.I)

    def is_image(self):
        return True if self.regex.search(self) else False

    def __iter__(self):
        for f in super(ImagePath, self).__iter__():
            if f.is_image():
                yield f


class OCR(object):
    """
    https://googlecloudplatform.github.io/google-cloud-python/stable/vision-usage.html#text-detection
    """

    @property
    def text(self):
        return self._text

    @property
    def lines(self):
        return self.text.splitlines(False)

    @property
    def words(self):
        return self._words

    @property
    def flow(self):
        """This attempts to get rid of extraneous newlines

        NOTE -- this is just really terribly impelemented, it's like 2am and I'm
        tired and I've got no internet for some reason

        :returns: string, the text reflowed
        """
        ret = [""]
        line_lens = []
        lines = self.lines
        for l in lines:
            line_lens.append(len(l))

        line_lens.sort()
        # we're interested in the longest lines, not the shortest
        half_i = int(len(line_lens) / 2)
        avg_len = int(sum(line_lens[half_i:]) / half_i)
        #avg_len = int(sum(line_lens) / len(line_lens))
        modifier = 0.4
        min_len = avg_len - int(avg_len * modifier)
        max_len = avg_len + int(avg_len * modifier)
        #pout.v(avg_len, min_len, max_len)

        for l in lines:
            line_len = len(l)
            # ??? -- would it be worth looking at punctuation at the end of the
            # line, if it has it then split, otherwise append
            if line_len >= min_len and line_len <= max_len:
                ret[-1] += " " + l
            else:
                ret[-1] += " " + l
                ret.append("") # new line

        return "\n".join(ret)

    def __init__(self, path):
        self.path = ImagePath(path)
        if not self.path.is_image():
            raise ValueError("{} is not an image path".format(path))

    def scan(self):
        client = vision.Client()
        image = client.image(content=self.path.contents())
        self.results = image.detect_text()

        self._text = ""
        self._words = None
        if self.results:
            self._text = self.results[0].description
            self._words = (w.description for w in self.results[1:])

        return self.results


