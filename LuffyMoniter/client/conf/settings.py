#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

# 远端服务器配置
Params = {
    "server": "127.0.0.1",
    "port": 8000,
    'url': '/report/',
    'request_timeout': 30,
}

# 日志文件配置

PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于API认证的请求头
AUTH_KEY_NAME = 'auth-key'

# 数据库采集
db_params = {
    "url":'jdbc:oracle:thin:@192.168.2.128:1521:PROD',
    "user":'scott',
    "password":'tiger',
    "driver":'oracle.jdbc.driver.OracleDriver',
    "jarFile":'D:\\instantclient_11_2\\ojdbc6.jar'
}
