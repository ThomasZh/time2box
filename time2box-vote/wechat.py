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
import logging

from tornado.escape import json_decode
from tornado.httpclient import HTTPClient


APP_ID = "wxaa328c83d3132bfb"
APP_SECRET = "32bbf99a46d80b24bae81e8c8558c42f"
DOMAIN = "planc2c.com"


def getAccessToken(appId, appSecret, code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appId+"&secret="+appSecret+"&code="+code+"&grant_type=authorization_code"
    http_client = HTTPClient()
    response = http_client.fetch(url, method="GET")
    logging.info("got response %r", response.body)
    accessToken = json_decode(response.body)
    return accessToken


def getUserInfo(token, openid):
    url = "https://api.weixin.qq.com/sns/userinfo?access_token="+token+"&openid="+openid+"&lang=zh_CN"
    http_client = HTTPClient()
    response = http_client.fetch(url, method="GET")
    logging.info("got response %r", response.body)
    userInfo = json_decode(response.body)
    return userInfo
