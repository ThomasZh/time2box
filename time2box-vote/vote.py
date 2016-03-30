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

import logging
import time

from tornado.escape import json_decode, json_encode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import tornado.web

from base import BaseHandler, STP


class VoteIndexHandler(tornado.web.RequestHandler):
    def get(self):
        _timestamp = long(time.time() * 1000)
        params = {"before":_timestamp, "limit":20}
        url = url_concat("http://"+STP+"/votes", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _votes = json_decode(response.body)
        
        self.render('vote/posts_index.html', votes=_votes)


class VoteMineHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _ticket = self.get_secure_cookie("ticket")
        
        _timestamp = long(time.time() * 1000)
        params = {"X-Session-Id": _ticket, "before":_timestamp, "limit":20}
        url = url_concat("http://"+STP+"/votes/mine", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _votes = json_decode(response.body)
        
        self.render('vote/posts_mine.html', votes=_votes)


class VoteInfoHandler(tornado.web.RequestHandler):
    def get(self):
        _vote_id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _vote_id)
        
        url = "http://"+STP+"/votes/" + _vote_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _vote = json_decode(response.body)
        
        self.render('vote/vote_info.html', vote=_vote)

    def post(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("id: ", _id)
        print _id
        _idx = (self.request.arguments['idx'])[0]
        print _idx
        logging.info("_idx: ", _idx)
        
        params = {"id": _id, "idx": _idx}
        url = "http://"+STP+"/votes/"+_id+"/"+_idx
        http_client = HTTPClient()
        _json = json_encode(params)
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)
        
        self.redirect("/vote/result?id="+_id)


class VoteResultHandler(tornado.web.RequestHandler):
    def get(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)

        url = "http://"+STP+"/votes/" + _id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _vote = json_decode(response.body)
        
        self.render('vote/vote_result.html', vote=_vote)


class VoteAdminPostHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self):
        _ticket = self.get_secure_cookie("ticket")
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        
        self.redirect("/vote/info?id="+_id)


class VoteAdminAddHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('vote/vote_add.html')
        
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _title = (self.request.arguments['title'])[0]
        _sub_title = (self.request.arguments['subTitle'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("_title: ", _title)
        logging.info("_sub_title: ", _sub_title)
        logging.info("_img_url: ", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://"+STP+"/votes", params)
        http_client = HTTPClient()
        vote =  {"title":_title,"subTitle":_sub_title,"imgUrl":_img_url,"items":[]}
        _json = json_encode(vote)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _id = json_decode(response.body)
        
        self.redirect("/vote/admin/items?id="+_id)


class VoteAdminEditHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('vote/vote_edit.html')

    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        
        self.redirect("/vote/admin/items?id="+_id)


class VoteAdminItemsHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        
        url = "http://"+STP+"/votes/" + _id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _vote = json_decode(response.body)
        
        self.render('vote/vote_items.html', vote=_vote)


class VoteAdminItemHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        
        self.render('vote/vote_item_add.html', id=_id)

    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        _ticket = self.get_secure_cookie("ticket")
        _text = (self.request.arguments['text'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("_text: ", _text)
        logging.info("_img_url: ", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://"+STP+"/votes/"+_id, params)
        http_client = HTTPClient()
        vote_item =  {"text":_text,"imgUrl":_img_url}
        _json = json_encode(vote_item)
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        
        self.redirect("/vote/admin/items?id="+_id)

    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self):
        _id = (self.request.arguments['id'])[0]
        logging.info("_vote_id: ", _id)
        
        self.redirect("/vote/admin/items?id="+_id)
