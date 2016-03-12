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
import random
import time

from tornado.escape import json_encode, json_decode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat
import tornado.web

from base import BaseHandler, timestamp_datetime, datetime_timestamp


class MyArticlesHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
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
            
        self.render('blog/my-articles.html', articles=_articles)


class MyArticleHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)

        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId="")


class AddArticleHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        self.render('blog/add-article.html')
        
    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _title = (self.request.arguments['title'])[0]
        _content = (self.request.arguments['content'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("got title %r", _title)
        logging.info("got title %r", _content)
        logging.info("got title %r", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/articles", params)
        data = {"title": _title, "content": _content, "imgUrl": _img_url}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)

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
            
        self.render('blog/my-articles.html', articles=_articles)


class AddParagraphHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)
        
        self.render('blog/add-paragraph.html', articleId=_article_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _type = (self.request.arguments['type'])[0]
        _content = (self.request.arguments['content'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got type %r", _type)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs", params)
        data = {"articleId": _article_id, "type": _type, "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class AddParagraphAfterHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        _brother_id = (self.request.arguments['brotherId'])[0]
        logging.info("article_id: ", _article_id)
        
        self.render('blog/add-paragraph-after.html', articleId=_article_id, brotherId=_brother_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _type = (self.request.arguments['type'])[0]
        _content = (self.request.arguments['content'])[0]
        _brother_id = (self.request.arguments['brotherId'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got type %r", _type)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_brother_id+"/after", params)
        data = {"articleId": _article_id, "type": _type, "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class AddParagraphRawHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)
        
        self.render('blog/add-paragraph-raw.html', articleId=_article_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _content = (self.request.arguments['content'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs", params)
        data = {"articleId": _article_id, "type": "raw", "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class AddParagraphRawAfterHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)
        _brother_id = (self.request.arguments['brotherId'])[0]
        
        self.render('blog/add-paragraph-raw-after.html', articleId=_article_id, brotherId=_brother_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _content = (self.request.arguments['content'])[0]
        _brother_id = (self.request.arguments['brotherId'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_brother_id+"/after", params)
        data = {"articleId": _article_id, "type": "raw", "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class AddParagraphImgHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)
        
        self.render('blog/add-paragraph-img.html', articleId=_article_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got img %r", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs", params)
        data = {"articleId": _article_id, "type": "img", "content": _img_url}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class AddParagraphImgAfterHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        _brother_id = (self.request.arguments['brotherId'])[0]
        logging.info("article_id: ", _article_id)
        
        self.render('blog/add-paragraph-img-after.html', articleId=_article_id, brotherId=_brother_id)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        _brother_id = (self.request.arguments['brotherId'])[0]
        logging.info("got article_id %r", _article_id)
        logging.info("got img %r", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_brother_id+"/after", params)
        data = {"articleId": _article_id, "type": "img", "content": _img_url}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        logging.info("got response %r", response.body)
        _paragraph_id = json_decode(response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class EditParagraphHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("paragraph_id: ", _paragraph_id)
        
        url = "http://182.92.66.109/blogs/paragraphs/" + _paragraph_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraph = json_decode(response.body)
        
        self.render('blog/edit-paragraph.html', articleId=_article_id, paragraph=_paragraph)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['paragraphId'])[0]
        _type = (self.request.arguments['type'])[0]
        _content = (self.request.arguments['content'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        logging.info("got type %r", _type)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id, params)
        data = {"articleId": _article_id, "id": _paragraph_id, "type": _type, "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class EditParagraphRawHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("paragraph_id: ", _paragraph_id)
        
        url = "http://182.92.66.109/blogs/paragraphs/" + _paragraph_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraph = json_decode(response.body)
        
        self.render('blog/edit-paragraph-raw.html', articleId=_article_id, paragraph=_paragraph)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['paragraphId'])[0]
        _content = (self.request.arguments['content'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        logging.info("got content %r", _content)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id, params)
        data = {"articleId": _article_id, "id": _paragraph_id, "type": "raw", "content": _content}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class EditParagraphImgHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("paragraph_id: ", _paragraph_id)
        
        url = "http://182.92.66.109/blogs/paragraphs/" + _paragraph_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraph = json_decode(response.body)
        
        self.render('blog/edit-paragraph-img.html', articleId=_article_id, paragraph=_paragraph)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['paragraphId'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        logging.info("got img_url %r", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id, params)
        data = {"articleId": _article_id, "id": _paragraph_id, "type": "img", "content": _img_url}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)

        self.render('blog/my-article.html', article=_article, paragraphs=_paragraphs, scrollToParagraphId=_paragraph_id)


class UpParagraphHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id+"/up", params)
        http_client = HTTPClient()
        data = {"articleId": _article_id}
        _json = json_encode(data)
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)

        self.finish("ok")  


class DownParagraphHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id+"/down", params)
        http_client = HTTPClient()
        data = {"articleId": _article_id}
        _json = json_encode(data)
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)

        self.finish("ok")  


class DelParagraphHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _ticket = self.get_secure_cookie("ticket")
        _article_id = (self.request.arguments['articleId'])[0]
        _paragraph_id = (self.request.arguments['id'])[0]
        logging.info("got paragraph_id %r", _paragraph_id)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/paragraphs/"+_paragraph_id, params)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="DELETE")
        logging.info("got response %r", response.body)

        self.finish("ok")  


class EditArticleHandler(BaseHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)
        
        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        
        self.render('blog/edit-article.html', article=_article)

    def post(self):
        _ticket = self.get_secure_cookie("ticket")
        _id = (self.request.arguments['articleId'])[0]
        _title = (self.request.arguments['title'])[0]
        _content = (self.request.arguments['content'])[0]
        _img_url = (self.request.arguments['imgUrl'])[0]
        logging.info("got title %r", _title)
        logging.info("got title %r", _content)
        logging.info("got title %r", _img_url)
        
        params = {"X-Session-Id": _ticket}
        url = url_concat("http://182.92.66.109/blogs/articles/"+_id, params)
        data = {"title": _title, "content": _content, "imgUrl": _img_url}
        _json = json_encode(data)
        http_client = HTTPClient()
        response = http_client.fetch(url, method="PUT", body=_json)
        logging.info("got response %r", response.body)

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
            
        self.render('blog/my-articles.html', articles=_articles)


class ArticleHandler(tornado.web.RequestHandler):
    def get(self):
        _article_id = (self.request.arguments['id'])[0]
        logging.info("article_id: ", _article_id)

        url = "http://182.92.66.109/blogs/articles/" + _article_id
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _article = json_decode(response.body)
        _timestamp = _article["timestamp"]
        _datetime = timestamp_datetime(_timestamp / 1000)
        _article["timestamp"] = _datetime
        
        url = "http://182.92.66.109/blogs/my-articles/" + _article_id + "/paragraphs"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="GET")
        logging.info("got response %r", response.body)
        _paragraphs = json_decode(response.body)
        
        _random = random.randint(1, 9)
        _bgImgRandom = "/static/images/title-bkg/"+str(_random)+".jpg"
        self.render('blog/article.html', article=_article, paragraphs=_paragraphs, bgImgRandom = _bgImgRandom)


class AjaxArticlesHandler(tornado.web.RequestHandler):
    def get(self):
        _last_timestamp = (self.request.arguments['last'])[0] # datetime as 2016-02-12 15:29
        print "last_timestamp: "+_last_timestamp
        
        if _last_timestamp == None:
            _timestamp = long(time.time() * 1000)
            print _timestamp
        elif _last_timestamp == '':
            _timestamp = long(time.time() * 1000)
            print _timestamp
        else:
            _timestamp = datetime_timestamp(_last_timestamp) * 1000
            print _timestamp
        
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
        
        self.finish(json.dumps(_articles))  


class AjaxMyArticlesHandler(tornado.web.RequestHandler):
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
