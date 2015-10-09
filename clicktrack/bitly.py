#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-10 09:30:12
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-10-05 11:23:51

import datetime as dt
import os

import requests as rq
from bitly_api import Connection
import yaml

import warnings
warnings.simplefilter('ignore')

# Config for this module is under 'bitly'; eg
# cat ~/.clicktrack (YAML)
# bitly
#     token: ...
#     ...

DEFAULT_CONFIG = os.path.expanduser('~/.clicktrack')

TODAY = dt.date.today().strftime("%Y-%m-%d")
YESTERDAY = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")


def get_page_urls(base_url=None, access_token=None, limit=None, config=None):
    '''Docs...'''
    config = os.path.expanduser(config or DEFAULT_CONFIG)
    with open(config) as _:
        _config = yaml.load(_) or {}
        conf = _config.get('bitly') or {}

    access_token = access_token or conf.get('access_token')
    bitly = Connection(access_token=access_token)

    data = bitly.user_link_history()

    for link in data:
        link['clicks_total'] = bitly.link_clicks(link['aggregate_link'])
        link['link_encoders_count'] = bitly.link_encoders_count(
            link['aggregate_link'])['count']

    # include timestamp filters
    return data
