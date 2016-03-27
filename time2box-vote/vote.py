#!/usr/bin/env python
#
# Copyright 2016 Time2Box
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

import json
import logging
import time

from tornado.escape import json_decode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import tornado.web

from base import BaseHandler, timestamp_datetime, datetime_timestamp


class VoteIndexHandler(tornado.web.RequestHandler):
    def get(self):
        _vote_id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _vote_id)
        
        self.render('vote/index.html')


class VoteResultHandler(tornado.web.RequestHandler):
    def get(self):
        _vote_id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _vote_id)

        self.render('vote/result.html')


class VoteAdminIndexHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('vote/admin_index.html')


class VoteAdminAddHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('vote/admin_add.html')
        
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):            
        self.render('vote/admin_index.html')


class VoteAdminAjaxHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _ticket = self.get_secure_cookie("ticket")
        _last_timestamp = (self.request.arguments['last'])[0] # datetime as 2016-02-12 15:29
        print _last_timestamp
        
        if _last_timestamp == None:
            _timestamp = long(time.time() * 1000)
            print _timestamp
        elif _last_timestamp == '':
            _timestamp = long(time.time() * 1000)
            print _timestamp
        else:
            _timestamp = datetime_timestamp(_last_timestamp) * 1000
            print _timestamp
        
        params = {"X-Session-Id": _ticket, "before": _timestamp, "limit": 20}
        url = url_concat("http://182.92.66.109/blogs/my-articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _articles = json_decode(response.body)
        
        for _article in _articles:
            _timestamp = _article["timestamp"]
            _datetime = timestamp_datetime(_timestamp / 1000)
            _article["timestamp"] = _datetime
        
        self.finish(json.dumps(_articles))  
