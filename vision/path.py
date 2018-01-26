# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os


class Path(str):
    def __new__(cls, path):
        path = os.path.abspath(os.path.expanduser(path))
        return super(Path, cls).__new__(cls, path)

    def is_file(self):
        return os.path.isfile(self)

    def is_dir(self):
        return os.path.isdir(self)

    def contents(self):
        if not self.is_file():
            raise RuntimeError("Trying to get the contents of a non-file")

        mode = "rb"
        with open(self, mode=mode) as fp:
            return fp.read()

    def __iter__(self):
        if self.is_file():
            yield self

        elif self.is_dir():
            for basedir, directories, files in os.walk(self, topdown=True):
                for basename in files:
                    path = os.path.join(basedir, basename)
                    yield type(self)(path)

        else:
            raise RuntimeError("Trying to iterate a non-directory or non-file")

