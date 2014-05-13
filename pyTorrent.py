# -*- coding: utf-8 -*-

import os
import sys
import socket
import time
import string
import getopt
import threading

from torrent import *

DEFAULT_PORT = 6881
DEFAULT_CACHESIZE = 32


class task(object):
    torrent = ""

    def __init__(self, filename):
        super(task, self).__init__()

        try:
            self.torrent = torrent(filename=torrent_file)
        except Exception, e:
            raise e
        

    def start():
        pass

    def stop():
        pass


def print_torrent_info(torrent_file):
    for torrent_key in torrent_file.keys():
        if torrent_key != "info":
            print torrent_key + ":" + str(torrent_file[torrent_key])

    print "=====info====="

    for info_key in torrent_file.info.keys():
        if info_key != "pieces":
            print info_key + ":" + str(torrent_file.info[info_key])
        else:
            print info_key + ":" + str(len(torrent_file.info[info_key]))


def main(torrent_file="", savepath="", port=DEFAULT_PORT, cache=32):
    trackers = []
    files = []
    pieces = []

    try:
        bit_torrent = torrent(filename=torrent_file)
    except Exception, e:
        raise e

    trackers = bit_torrent.get_trackers()
    pieces = bit_torrent.get_pieces()
    # print_torrent_info(bit_torrent)

if __name__ == '__main__':
    torrent_file = ""
    save_path = ""
    cache_size = DEFAULT_CACHESIZE
    port = DEFAULT_PORT

    opts, args = getopt.getopt(
        sys.argv[1:],
        't:s:p:c:',
        ["torrent=", "savepath=", "port=", "cache="],
    )

    for arg, value in opts:
        if arg in ('-t', '--torrent'):
            torrent_file = value
        if arg in ('-s', '--savepath'):
            save_path = value
        if arg in ('-p', '--port'):
            port = int(value)
        if arg in ('-c', '--cache'):
            cache_size = int(value)

    main(torrent_file, save_path, port, cache_size)
