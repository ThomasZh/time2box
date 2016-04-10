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

import os.path

import tornado.ioloop
from tornado.options import define, options, parse_command_line
from tornado.web import RequestHandler
import tornado.web

from account import LoginHandler, LogoutHandler, RegisterHandler, \
    ForgotPwdHandler, ResetPwdHandler
from shop import ShopIndexHandler, ShopProductHandler, ShopProductDetailsHandler, \
    ShopCheckoutHandler, ShopCartHandler, ShopLoginHandler, ShopContactUsHandler, \
    ShopBlogHandler, ShopBlogSingleHandler


define("port", default=8896, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class PageNotFoundHandler(RequestHandler):
    def get(self):
        self.render('shop/404.html')


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", ShopIndexHandler),
            (r'/account/login', LoginHandler),
            (r'/account/logout', LogoutHandler),
            (r'/account/register', RegisterHandler),
            (r'/account/forgot-pwd', ForgotPwdHandler),
            (r'/account/reset-pwd', ResetPwdHandler),
            (r'/shop/index', ShopIndexHandler),
            (r'/shop/product', ShopProductHandler),
            (r'/shop/product-details', ShopProductDetailsHandler),
            (r'/shop/checkout', ShopCheckoutHandler),
            (r'/shop/cart', ShopCartHandler),
            (r'/shop/login', ShopLoginHandler),
            (r'/shop/contact-us', ShopContactUsHandler),
            (r'/shop/blog', ShopBlogHandler),
            (r'/shop/blog-single', ShopBlogSingleHandler),
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
