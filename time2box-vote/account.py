#!/usr/bin/env python
#
# Copyright 2015 planc2c.com
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

import base64
from gettext import gettext as _
import logging
import uuid

from tornado.escape import json_encode, json_decode
from tornado.httpclient import HTTPClient

from base import BaseHandler, STP


class LoginHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        _login_name = self.get_secure_cookie("login_name")
        if _login_name == None:
            _login_name = ""
        _remember_me = self.get_secure_cookie("remember_me")
        if _remember_me == None:
            _remember_me = "off"
        print "login_name: "+_login_name
        print "remember_me: " + _remember_me
        self.render('account/login.html', err_msg="", login_name=_login_name, remember_me=_remember_me)

    def post(self):
        _login_name = self.get_argument("input-email")
        _md5pwd = self.get_argument("input-password")
        _remember_me = self.get_argument("remember-me", "off")
        _user_agent = self.request.headers["User-Agent"]
        _user_locale = self.request.headers["Accept-Language"]
        _device_id = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        print "login_name: "+_login_name
        print "remember_me: " + _remember_me
        print  "user_locale: " + _user_locale
        
        try:
            params = { "osVersion" : "webkit:"+_user_agent,
                  "gateToken" : "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                  "deviceId" : _device_id,
                  "password" : _md5pwd,
                  "email" : _login_name}
            _json = json_encode(params)
            url = "http://"+STP+"/account/login"
            http_client = HTTPClient()
            response = http_client.fetch(url, method="POST", body=_json)
            print response.body
            _stp_session = json_decode(response.body)
            _session_ticket = _stp_session["sessionToken"]
            
            self.set_secure_cookie("ticket", _session_ticket)
            self.set_secure_cookie("login_name", _login_name)
            self.set_secure_cookie("remember_me", _remember_me)
            self.redirect("/")
        except Exception:  
            _err_msg = _("Please enter a correct username and password.")
            self.render('account/login.html', err_msg=_err_msg, 
                        login_name=_login_name, remember_me=_remember_me)


class LogoutHandler(BaseHandler):
    def get(self):
        _remember_me = self.get_secure_cookie("remember_me")
        if _remember_me == None:
            _remember_me = "off"
        print  _remember_me
        
        if _remember_me == "off":
            self.clear_cookie("ticket")
            self.clear_cookie("login_name")
            self.clear_cookie("remember_me")
        else:
            self.clear_cookie("ticket")
        self.redirect("/")


class RegisterHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        self.render('account/register.html', err_msg="")

    def post(self):
        _email = self.get_argument("input-email")
        _md5pwd = self.get_argument("input-password")
        _user_agent = self.request.headers["User-Agent"]
        _lang = self.request.headers["Accept-Language"]
        _device_id = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        print _email
        print _md5pwd
        print _user_agent
        print _lang
    
        try:
            params = { "osVersion" : "webkit:"+_user_agent,
                  "gateToken" : "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                  "deviceId" : _device_id,
                  "md5pwd" : _md5pwd,
                  "email" : _email,
                  "lang": _lang,}
            _json = json_encode(params)
            url = "http://"+STP+"/account/email-register"
            http_client = HTTPClient()
            response = http_client.fetch(url, method="POST", body=_json)
            print response.body
            _stp_session = json_decode(response.body)
            _sessionTicket = _stp_session["sessionToken"]
            
            self.set_secure_cookie("ticket", _sessionTicket)
            self.set_secure_cookie("login_name", _email)
            self.redirect("/")
        except Exception:  
            _err_msg = _("Email already exist, please try another.")
            self.render('account/register.html', err_msg=_err_msg)


class ForgotPwdHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        _email = self.get_secure_cookie("login_name")
        if _email == None:
            _email = ""
        self.render('account/forgot-pwd.html', login_name=_email)

    def post(self):
        _email = self.get_argument("input-email", "")
        print _email
        
        params = {"email" : _email}
        _json = json_encode(params)
        url = "http://"+STP+"/account/apply-for-email-verification"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        print response.body

        _err_msg = _("Email has been send to your mail, please check it.")
        self.render('account/login.html', err_msg=_err_msg, 
                    login_name=_email, remember_me="on")    


class ResetPwdHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        _ekey = self.get_argument("ekey", "")
        self.render('account/reset-pwd.html', ekey=_ekey)

    def post(self):
        _ekey = self.get_argument("ekey", "")
        _md5pwd = self.get_argument("input-password", "")
        print _ekey
        
        params = {"ekey" : _ekey}
        _json = json_encode(params)
        url = "http://"+STP+"/account/verify-email"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        print response.body
        _ekey_object = json_decode(response.body)
        _email = _ekey_object["email"]

        params = {"ekey" : _ekey, "email": _email, "newPassword": _md5pwd}
        _json = json_encode(params)
        url = "http://"+STP+"/account/reset-password"
        http_client = HTTPClient()
        response = http_client.fetch(url, method="POST", body=_json)
        print response.body
        
        _err_msg = _("Password has been changed, please sign in.")
        self.render('account/login.html', err_msg=_err_msg, 
                    login_name="", remember_me="off")


def ssoLogin(loginType, loginName, nickname, avatarUrl, userAgent, lang):
    _device_id = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    params = {"gateToken" : "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=", "deviceId": _device_id, "osVersion" : "webkit:"+userAgent, "loginType": loginType, "loginName": loginName, "nickname": nickname, "imageUrl" : avatarUrl, "lang" : lang}
    _json = json_encode(params)
    url = "http://"+STP+"/account/ssologin"
    http_client = HTTPClient()
    response = http_client.fetch(url, method="POST", body=_json)
    logging.info("got response %r", response.body)
    stpSession = json_decode(response.body)
    return stpSession
