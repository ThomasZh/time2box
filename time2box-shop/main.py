#!/usr/bin/env python
# -*- coding:utf-8 -*-
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


class MyErrorHandler(RequestHandler):
    def get_error_html(self, status_code=500, **kwargs):
        error_info = dict()
        error_info = kwargs
        error_info['url'] = self.request.protocol + "://" + self.request.host + self.request.uri
        error_info['code'] = status_code
        #error_info['debug'] = AFWConfig.afewords_debug
    
        logging.error(error_info['exc_info'])
        logging.error('Url Error %s' % self.request.uri)
        
        if 'title' not in error_info:
            title = '迷路了 - 子曰'
    
        if "des" not in error_info:
            if status_code >=500:
                error_info['des'] = '抱歉，服务器出错！请您将这里的信息复制并作为反馈提交给我们，我们将尽快修复这个问题！'
            else:
                error_info['des'] = "开发人员未给出具体描述！"
    
        if "next_url" not in error_info:
            error_info['next_url'] = '/'
    
        if "exc_info" not in error_info:
            if "my_exc_info" not in error_info:
                if status_code >=500:
                    error_info['exc_info'] = '抱歉，服务器出错！'
                else:
                    error_info['exc_info'] = '错误栈未传入错误输出程序！'
            else:
                error_info['exc_info'] = error_info['my_exc_info']
        if "reason" not in error_info:
            error_info['reason'] = [error_info['des']]

        if status_code >= 500:
            logging.error(error_info['exc_info'])
            logging.error('Url Error %s' % self.request.uri)
    
        return self.render_string("error.html", error=error_info)


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
            (".*", MyErrorHandler),
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
