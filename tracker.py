#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import struct
import urllib
import urllib2

import util

from bencode import *


DEFALUT_PORT = 6881


class CommonTrackerFailure(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NerworkFailure(CommonTrackerFailure):
    pass


class ServerFailure(CommonTrackerFailure):
    pass


class ResponseFailure(CommonTrackerFailure):
    pass


def parse_compact_peers(peers):
    ip = ""
    port = 0
    lst = []

    peer_lst = [peers[x:x + 6] for x in range(0, len(peers), 6)]
    for peer in peer_lst:
        ret = struct.unpack("5I", peer)
        ip = str(ret[0]) + str(ret[1]) + str(ret[2]) + str(ret[3])
        port = ret[5]
        lst.append({"peer id": "", "ip": ip, "port": port})
    return lst


class tracker(object):
    peer_id = ""
    host = ""
    listen_port = 6881
    interval = 0

    __last_check_timestamp__ = 0

    def __init__(self, host, peer_id, listen_port):
        super(tracker, self).__init__()
        self.host = host
        self.peer_id = peer_id
        self.listen_port = listen_port

    def update(self, info_hash, uploaded, downloaded, compact, left, event):
        values = {
            "info_hash": info_hash,
            "peer_id": self.peer_id,
            "port": self.listen_port,
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left,
            "compact": compact?1: 0,
            "event": event
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(self.host, data)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            raise NerworkFailure(e.reason)
        except urllib2.URLError, e:
            raise ServerFailure("%d,%s" % (e.code, e.read()))

        try:
            result = bdecode(response)
        except BTFailure:
            raise ResponseFailure("bdecode error.")

        if result.has_key("failure reason"):
            raise ServerFailure(result["ResponseFailure"])

        self.__last_check_timestamp__ = util.timestamp()
        self.interval = result["Interval"]

        if compact:
            return parse_compact_peers(result["Peers"])

        return result["Peers"]

    def check_interval(self):
        curtime = util.timestamp()
        if curtime - self.__last_check_timestamp__ < self.interval:
            return False

        return True
