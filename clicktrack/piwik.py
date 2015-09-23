#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-10 09:30:12
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-23 14:01:07

import datetime as dt
import os
import re
import json

import requests as rq
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
import yaml

import warnings
warnings.simplefilter('ignore')

TODAY = dt.date.today().strftime("%Y-%m-%d")
YESTERDAY = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")

def get_page_urls(filter_pattern, domain=None, site_id=None, date=(YESTERDAY, TODAY), period='range',
                  data_format='json', limit=-1, expanded=True,
                  filter_column='label', show_columns=None, total=False,
                  hide_columns=None):
    '''Docs...'''
    if domain is None:
        raise TypeError("Domain should be provided")
    if site_id is None:
        raise TypeError("SiteId should be provided")

    '''list all available columns in the documentation strings'''
    payload = {'module': 'API',
               'method': 'Actions.getPageUrls',
               'format': data_format,
               'idSite': site_id,
               'period': period,
               'date': '%s,%s' % date,
               'expanded': int(expanded),
               'filter_limit': limit,
               'translateColumnNames': True,
               'language': 'en',
               'filter_column': filter_column,
               'filter_pattern': filter_pattern,
               'showColumns': ','.join(show_columns) if show_columns else None,
               'hideColumns': ','.join(hide_columns) if hide_columns else None}

    auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    data = rq.get(domain,
                  params=payload,
                  verify=False,
                  auth=auth).text

    if data_format == 'json':
        data = json.loads(data)
        # data = {key: [l[key] for l in data]for key in data[0].keys()}

    if type(data) is dict and data["result"] == 'error':
        raise RuntimeError(
            "You can't access this resource as it requires an 'view' access for the website id = %d" % (site_id))

    return data

if __name__ == '__main__':
    "Example"
    CONFIG_FILE = os.path.expanduser('examples/config/piwik')
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    repo_path = os.path.dirname(dir_path)

    if os.path.join(repo_path, CONFIG_FILE):
        with open(os.path.join(repo_path, CONFIG_FILE)) as _:
            config = yaml.load(_)
    else:
        config = {}

    print get_page_urls(filter_pattern=None, show_columns=['label', 'nb_hits', 'nb_visits'], **config)

