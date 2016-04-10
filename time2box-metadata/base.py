#!/usr/bin/env python
#
# Copyright 2015 Time2Box
# thomas@time2box.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import time

import tornado.web

STP = "123.56.228.41"


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("ticket")


def timestamp_datetime(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%Y-%m-%d %H:%M'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


def datetime_timestamp(dt):
     # dt is string
     time.strptime(dt, '%Y-%m-%d %H:%M')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     # "2012-03-28 06:53:40" to timestamp(int)
     _timestamp = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M'))
     return int(_timestamp)