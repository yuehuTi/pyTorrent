#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import struct
import hashlib
from bencode import *

SHA1_LEN = 20


class torrent(dict):

    def __init__(self, filename=""):
        try:
            btfile = open(filename, "rb")
            filecontent = btfile.read()
            tordict = bdecode(filecontent)
            btfile.close()

            for k, v in tordict.iteritems():
                self[str(k)] = v
            self.filename = filename

        except Exception, e:
            raise e

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'Torrent' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def is_multifiles(self):
        return self.info.has_key("files")

    def get_files(self):
        folder = ""
        files = []
        dstfile = {}
        piece_lenght = self.info["piece length"]
        if self.isMultifiles():
            for single_file in self.info.files:
                dstfile["path"] = single_file.path
                dstfile["length"] = single_file.length
        else:
            dstfile["path"] = self.info.name
            dstfile["length"] = self.info.length

    def get_pieces(self):
        return [self.info.pieces[x:x + SHA1_LEN] for x in range(0, len(self.info.pieces), SHA1_LEN)]

    def get_trackers(self):
        trackers = []
        if self.has_key("announce-list"):
            for server in self["announce-list"]:
                trackers.append(server[0])
        trackers.append(self["announce"])
        return trackers


def unit_teset():
    bt_file = torrent("test.torrent")
    print bt_file.get_pieces()

if __name__ == '__main__':
    unit_teset()
