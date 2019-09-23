# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import datetime
import re
from datetime import timedelta

from .compat import *


class Time(timedelta):
    """Prints time in the format of HH:MM:SS, it will also parse values and normalize
    their values"""
    @property
    def minutes(self):
        return self.seconds // 60

    @property
    def hours(self):
        return self.seconds // 3600

    def __new__(cls, val):
    #def __init__(self, val):
        val = str(val)

        hours = minutes = seconds = 0
        negative = False

        if val:
            if val.startswith("-"):
                val = val[1:]
                negative = True

            if ":" in val:
                parts = list(map(int, val.split(":")))
                parts_count = len(parts)
                if parts_count == 3:
                    hours, minutes, seconds = parts
                elif parts_count == 2:
                    minutes, seconds = parts
                else:
                    raise ValueError("Invalid time {}, try H:MM:SS or NmNs or N".format(val))

            else:
                ms = re.findall(r"(\d+)([hms])", val, re.I)
                if ms:
                    for n, d in ms:
                        d = d.lower()
                        if d == 'h':
                            hours = int(n)
                        elif d == 'm':
                            minutes = int(n)
                        elif d == 's':
                            seconds = int(n)

                else:
                    # https://stackoverflow.com/a/775075/5006
                    if "." in val:
                        val = float(val)
                    m, s = divmod(int(val), 60)
                    h, m = divmod(m, 60)
                    hours = h
                    minutes = m
                    seconds = s

        instance = super(Time, cls).__new__(
            cls,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )

        instance.negative = negative
        return instance

    def __str__(self):
        s = super(Time, self).__str__()
        if self.negative:
            s = "-{}".format(s)
        return s

    def total_seconds(self):
        ret = super(Time, self).total_seconds()
        if self.negative:
            ret *= -1
        return ret

    def total_ms(self):
        s = self.total_seconds()
        return s * 1000

    def __format__(self, formatstr):
        return "{{:{}}}".format(formatstr).format(self.__str__())


class ByteString(Bytes):
    """Wrapper around a byte string b"" to make sure we have a byte string that
    will work across python versions and handle the most annoying encoding issues
    automatically

    :Example:
        # python 3
        s = ByteString("foo)
        str(s) # calls __str__ and returns self.unicode()
        unicode(s) # errors out
        bytes(s) # calls __bytes__ and returns ByteString
        # python 2
        s = ByteString("foo)
        str(s) # calls __str__ and returns ByteString
        unicode(s) # calls __unicode__ and returns String
        bytes(s) # calls __str__ and returns ByteString
    """
    def __new__(cls, val=b"", encoding="UTF-8"):
        if isinstance(val, type(None)): return None

        if not isinstance(val, (bytes, bytearray)):
            if is_py2:
                val = unicode(val)
            else:
                val = str(val)
            #val = val.__str__()
            val = bytearray(val, encoding)

        instance = super(ByteString, cls).__new__(cls, val)
        instance.encoding = encoding
        return instance

    def __str__(self):
        return self if is_py2 else self.unicode()

    def unicode(self):
        s = self.decode(self.encoding)
        return String(s)
    __unicode__ = unicode

    def bytes(self):
        return self
    __bytes__ = bytes

    def raw(self):
        """because sometimes you need a vanilla bytes()"""
        return b"" + self


class String(Str):
    @property
    def lines(self):
        return self.splitlines(False)

    def __new__(cls, val="", encoding="UTF-8"):
        if isinstance(val, type(None)): return None

        if not isinstance(val, Str):
            val = ByteString(val, encoding).unicode()

        instance = super(String, cls).__new__(cls, val)
        instance.encoding = encoding
        return instance

    def __str__(self):
        return self.bytes() if is_py2 else self

    def unicode(self):
        return self
    __unicode__ = unicode

    def bytes(self):
        s = self.encode(self.encoding)
        return ByteString(s)
    __bytes__ = bytes

    def raw(self):
        """because sometimes you need a vanilla str() (or unicode() in py2)"""
        return "" + self

    def flow(self):
        """This attempts to get rid of extraneous newlines

        NOTE -- this is just really terribly impelemented, it's like 2am and I'm
        tired and I've got no internet for some reason

        :returns: string, the text reflowed
        """
        line_lens = []
        lines = self.lines
        for l in lines:
            line_lens.append(len(l))

        line_lens.sort()
        # we're interested in the longest lines, not the shortest
        if len(line_lens) > 1:
            ret = [""]
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

            ret = type(self)("\n".join(ret))

        else:
            ret = lines[0]

        return type(self)(ret)

