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

import logging
import os.path
import time

from tornado.escape import json_decode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import tornado.ioloop
from tornado.options import define, options, parse_command_line
from tornado.web import RequestHandler
import tornado.web

from account import LoginHandler, LogoutHandler, RegisterHandler, \
    ForgotPwdHandler, ResetPwdHandler
from base import timestamp_datetime
from blog import AddArticleHandler, ArticleHandler, AjaxArticlesHandler, \
    MyArticlesHandler, EditArticleHandler, AjaxMyArticlesHandler, \
    MyArticleHandler, AddParagraphHandler, EditParagraphHandler, \
    UpParagraphHandler, DownParagraphHandler, EditParagraphRawHandler, \
    EditParagraphImgHandler, AddParagraphRawHandler, AddParagraphImgHandler, \
    DelParagraphHandler, AddParagraphAfterHandler, AddParagraphRawAfterHandler, \
    AddParagraphImgAfterHandler

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class PageNotFoundHandler(RequestHandler):
    def get(self):
        self.render('404.html')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        _timestamp = long(time.time() * 1000)
        params = {"before": _timestamp, "limit": 20}
        url = url_concat("http://182.92.66.109/blogs/articles", params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _articles = json_decode(response.body)
        
        for _article in _articles:
            _timestamp = _article["timestamp"]
            _datetime = timestamp_datetime(_timestamp / 1000)
            _article["timestamp"] = _datetime
        
        self.render('index.html', articles=_articles)


class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('about.html')


class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('contact.html')


def main():
    parse_command_line()
    app = tornado.web.Application(
        [            
            (r"/", MainHandler),
            (r"/about", AboutHandler),
            (r"/contact", ContactHandler),
            (r"/article", ArticleHandler),
            (r"/ajax-articles", AjaxArticlesHandler),
            (r"/ajax-my-articles", AjaxMyArticlesHandler),
            (r'/account/login', LoginHandler),
            (r'/account/logout', LogoutHandler),
            (r'/account/register', RegisterHandler),
            (r'/account/forgot-pwd', ForgotPwdHandler),
            (r'/account/reset-pwd', ResetPwdHandler),
            (r"/admin/my-articles", MyArticlesHandler),
            (r"/admin/my-article", MyArticleHandler),
            (r"/admin/add-article", AddArticleHandler),
            (r"/admin/edit-article", EditArticleHandler),
            (r"/admin/add-paragraph", AddParagraphHandler),
            (r"/admin/add-paragraph-raw", AddParagraphRawHandler),
            (r"/admin/add-paragraph-img", AddParagraphImgHandler),
            (r"/admin/add-paragraph/after", AddParagraphAfterHandler),
            (r"/admin/add-paragraph-raw/after", AddParagraphRawAfterHandler),
            (r"/admin/add-paragraph-img/after", AddParagraphImgAfterHandler),
            (r"/admin/edit-paragraph", EditParagraphHandler),
            (r"/admin/edit-paragraph-raw", EditParagraphRawHandler),
            (r"/admin/edit-paragraph-img", EditParagraphImgHandler),
            (r"/admin/paragraph/up", UpParagraphHandler),
            (r"/admin/paragraph/down", DownParagraphHandler),
            (r"/admin/paragraph/del", DelParagraphHandler),
            (".*", PageNotFoundHandler),
            ],
        # __TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        login_url="/account/login",
        )
    tornado.locale.load_gettext_translations(os.path.join(os.path.dirname(__file__), "locale"), "stickynote")
    tornado.locale.set_default_locale("en_US")
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
