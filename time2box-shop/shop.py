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

import tornado.web


class ShopIndexHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/index.html')


class ShopProductHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/shop.html')


class ShopProductDetailsHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/product-details.html')


class ShopCheckoutHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/checkout.html')


class ShopCartHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/cart.html')


class ShopLoginHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/login.html')


class ShopContactUsHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/contact-us.html')


class ShopBlogHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/blog.html')


class ShopBlogSingleHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render('shop/blog-single.html')