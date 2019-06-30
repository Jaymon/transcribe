# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
from unittest import TestCase

from transcribe.image import OCR
from transcribe.utils import Time, String
from transcribe.path import TempPath, Path


class TOCR(OCR):
    def __init__(self, text):
        self._text = text

    def scan(self):
        raise NotImplementedError()


class OCRTest(TestCase):
    pass

class StringTest(TestCase):
    def test_flow_oneline(self):
        s = String("but when we put the feed at the router be in a one or two shows already up there we hope you'll check it out my goal is to get you quite a bit more content than I've been getting you and if common sense just pops up in your feed don't be surprised because you know every now and then we get the band back together man")

        pout.v(s.flow())

    def test_flow_multiline(self):
        s = String("""Horst Rittel and Melvin Webber defined a "wicked" problem as one that could be
clearly defined only by solving it, or by solving part of it (1973). This paradox implies,
essentially, that you have to "solve" the problem once in order to clearly define it and
then solve it again to create a solution that works. This process
and apple pie in software development for decades (Peters and Tripp 1976).
has been motherhood
In my part of the world, a dramatic example of such a wicked problem was the design
of the original Tacoma Narrows bridge. At the time the bridge was built, the main con-
sideration in designing a bridge was that it be strong enough to support its planned
load. In the case of the Tacoma Narrows bridge, wind created an unexpected, side-to-
side harmonic ripple. One blustery day in 1940, the ripple grew uncontrollably until
the bridge collapsed, as shown in Figure 5-1
This is a good example of a wicked problem because, until the bridge collapsed, its
engineers didn't know that aerodynamics needed to be considered to such an extent.
Only by building the bridge (solving the problem) could they learn about the addi-
tional consideration in the problem that allowed them to build another bridge that
still stands.
Copyrighted s
5.1 Design Challenges
75
Figure S-
ine iacoma Narrows briage -an example of a wickea probiem.
One of the main differences between programs you develop in school and those you
develop as a professional is that the design problems solved by school programs are
rarely, if ever, wicked. Programming assignments in school are devised to move you in a
beeline from beginning to end. You'd probably want to tar and feather a teacher who gave
you a programming assignment, then changed the assignment as soon as you finished
the design, and then changed it again just as you were about to turn in the completed pro-
gram. But that very process is an everyday reality in professional programming.""")

        pout.v(s.flow())

class TimeTest(TestCase):
    def test_syntax(self):
        t = Time("140")
        self.assertEqual("0:02:20", str(t))
        self.assertEqual(140, t.total_seconds())

        t = Time("-15m20s")
        self.assertEqual("-0:15:20", str(t))
        self.assertEqual(-920, t.total_seconds())

        t = Time("-15m")
        self.assertEqual("-0:15:00", str(t))
        self.assertEqual(-900, t.total_seconds())

        t = Time("-15:20")
        self.assertEqual("-0:15:20", str(t))
        self.assertEqual(-920, t.total_seconds())

    def test_literal(self):
        t = Time(204.442388058)
        self.assertEqual("0:03:24", str(t))
        self.assertEqual(204, t.total_seconds())

    def test_empty(self):
        t = Time('')
        self.assertEqual(0, t.total_seconds())

    def test_hhmmss(self):
        t = Time("00:01:00")
        self.assertEqual(1, t.minutes)
        self.assertEqual(0, t.hours)
        self.assertEqual(60, t.seconds)
        self.assertEqual(60, t.total_seconds())

    def test_format(self):
        t = Time(60)
        s = "{:<15}".format(t)
        self.assertEqual("0:01:00        ", s)


class PathTest(TestCase):
    def test_name(self):
        p = Path("~/some-random-317-name (last 10 minutes).mp3")
        self.assertEqual("some-random-317-name (last 10 minutes)", p.name)

    def test_safename(self):
        p = Path("~/some-random-317-name (last 10 minutes).mp3")
        self.assertEqual("some-random-317-name_last_10_minutes.mp3", p.safename)

    def test_temp(self):
        p = TempPath("foo", "txt")
        pout.v(p)

