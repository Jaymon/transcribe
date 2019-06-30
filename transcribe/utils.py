# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import datetime
import re
from datetime import timedelta


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

    def __format__(self, formatstr):
        return "{{:{}}}".format(formatstr).format(self.__str__())


class TimeBAK(object):
    """Prints time in the format of HH:MM:SS, it will also parse values and normalize
    their values"""
    @property
    def total_seconds(self):
        ret = self.hours * 3600
        ret += self.minutes * 60
        ret += self.seconds
        return -ret if self.negative else ret

    @property
    def total_ms(self):
        s = self.total_seconds
        return s * 1000

    def __init__(self, val):
        val = str(val)

        self.hours = self.minutes = self.seconds = 0
        self.negative = False

        if val:
            if val.startswith("-"):
                val = val[1:]
                self.negative = True

            if ":" in val:
                parts = list(map(int, val.split(":")))
                parts_count = len(parts)
                if parts_count == 3:
                    self.hours, self.minutes, self.seconds = parts
                elif parts_count == 2:
                    self.minutes, self.seconds = parts
                else:
                    raise ValueError("Invalid time {}, try H:MM:SS or NmNs or N".format(val))

            else:
                ms = re.findall(r"(\d+)([hms])", val, re.I)
                if ms:
                    for n, d in ms:
                        d = d.lower()
                        if d == 'h':
                            self.hours = int(n)
                        elif d == 'm':
                            self.minutes = int(n)
                        elif d == 's':
                            self.seconds = int(n)

                else:
                    # https://stackoverflow.com/a/775075/5006
                    if "." in val:
                        val = float(val)
                    m, s = divmod(int(val), 60)
                    h, m = divmod(m, 60)
                    self.hours = h
                    self.minutes = m
                    self.seconds = s

    def __str__(self):
        s = str(datetime.timedelta(seconds=abs(self.total_seconds)))
        #s = time.strftime('%H:%M:%S', time.gmtime(self.total_seconds))
        if self.negative:
            s = "-{}".format(s)
        return s

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __bool__(self):
        return self.hours > 0 or self.minutes > 0 or self.seconds > 0
    __nonzero__ = __bool__

    def __format__(self, formatstr):
        return "{{:{}}}".format(formatstr).format(self.__str__())


class String(str):
    @property
    def lines(self):
        return self.splitlines(False)

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

