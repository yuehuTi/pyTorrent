#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import datetime


def cover_size(size):
    gb = 1024 * 1024 * 1024
    mb = 1024 * 1024
    kb = 1024

    if size > gb:
        return str(float('%.3f' % (float(size) / gb))) + "GB"
    elif size > mb:
        return str(float('%.3f' % (float(size) / mb))) + "MB"
    elif size > kb:
        return str(float('%.3f' % (float(size) / kb))) + "KB"
    else:
        return str(size) + "B"


def timestamp():
    return time.mktime(datetime.datetime.now().timetuple())
