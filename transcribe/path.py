# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
import tempfile
import re
import mimetypes


class Path(str):
    @property
    def mimetype(self):
        mt = mimetypes.guess_type(self)[0]
        if mt is None:
            mt = ""
        return mt

    @property
    def name(self):
        root, ext = os.path.splitext(self.basename)
        return root

    @property
    def basename(self):
        return os.path.basename(self)

    @property
    def safename(self):
        name = self.basename
        for c in "({[]})":
            name = name.replace(c, "")
        #name = re.strip(r"[\(\)\{\}\[\]]", "", name)
        name = name.replace(" ", "_")
        return name

    @property
    def ext(self):
        root, ext = os.path.splitext(self)
        return ext.lstrip(".")

    def __new__(cls, path):
        path = os.path.abspath(os.path.expanduser(path))
        return super(Path, cls).__new__(cls, path)

    def stream(self, mode="r"):
        return open(self, mode=mode)

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

    def is_type(self):
        """Override this in child classes to decide if this file should be returned
        in the iterator"""
        return True

    def __iter__(self):
        if self.is_file():
            if self.is_type():
                yield self

        elif self.is_dir():
            for basedir, directories, files in os.walk(self, topdown=True):
                for basename in files:
                    path = os.path.join(basedir, basename)
                    instance = type(self)(path)
                    if instance.is_type():
                        yield instance

        else:
            raise RuntimeError("Trying to iterate a non-directory or non-file")


class TempPath(Path):
    """The idea of this class is to make it easy to create a filepath in the temp
    directory

    :Example:
        tp = TempPath("foo", "txt") # full path will be something like: /tmp/foo.txt
    """
    def __new__(cls, basename, ext=""):
        basedir = tempfile.gettempdir()
        if ext:
            basename = "{}.{}".format(basename, ext.lstrip("."))
        path = os.path.join(basedir, basename)
        return super(TempPath, cls).__new__(cls, path)


class Paths(object):
    def __init__(self, paths, path_cls=Path):
        self.paths = paths
        self.path_cls = path_cls

    def __iter__(self):
        for path in self.paths:
            p = self.path_cls(path)
            for f in p:
                yield p


