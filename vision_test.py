# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
from unittest import TestCase

from vision import OCR


class TOCR(OCR):
    def __init__(self, text):
        self._text = text

    def scan(self):
        raise NotImplementedError()


class VisionTest(TestCase):
    def test_flow(self):
        image = TOCR("""Horst Rittel and Melvin Webber defined a "wicked" problem as one that could be
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

        pout.v(image.flow)

