#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-10 09:30:12
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-23 14:01:07

import datetime as dt
import os

import requests as rq
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
import yaml

import warnings
warnings.simplefilter('ignore')

DEFAULT_CONFIG = os.path.expanduser('~/.clicktrack')
TODAY = dt.date.today().strftime("%Y-%m-%d")
YESTERDAY = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")


def get_page_urls(filter_pattern=None, domain=None, idSite=None, date=None,
                  period='range', format='json', filter_limit=-1, expanded=1,
                  filter_column='label', showColumns=None, total=False,
                  hideColumns=None, config=None):
    '''Docs...'''
    config = os.path.expanduser(config or DEFAULT_CONFIG)
    with open(config) as _:
        config = yaml.load(_)

    domain = domain or config.get('domain')
    idSite = idSite or config.get('idSite')
    if domain is None:
        raise TypeError("Domain should be provided")
    if idSite is None:
        raise TypeError("idSite should be provided")
    period = period or config.get('period')
    # expected as str YYYY-MM-DD,YYY-MM-DD
    date = date or config.get('date', '{},{}'.format(YESTERDAY, TODAY))
    expanded = int(expanded or config.get('expanded', 1))
    filter_limit = int(filter_limit or config.get('filter_limit', -1))
    filter_column = filter_column or config.get('filter_column', 'label')
    filter_pattern = filter_pattern or config.get('filter_pattern')
    showColumns = showColumns or config.get('showColumns')

    '''list all available columns in the documentation strings'''
    payload = {
        'module': 'API',
        'method': 'Actions.getPageUrls',
        'format': format or config.get('format'),
        'idSite': idSite,
        'period': period,
        'date': date,
        'expanded': expanded,
        'filter_limit': filter_limit,
        'translateColumnNames': True,
        'language': 'en',
        'filter_column': filter_column,
        'filter_pattern': filter_pattern,
        # eg, ['label', 'nb_hits', 'nb_visits']
        'showColumns': showColumns,
        'hideColumns': hideColumns,
    }

    auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    resp = rq.get(domain, params=payload, verify=False, auth=auth)

    if format == 'json':
        data = resp.json()
    else:
        data = resp.text

    if isinstance(data, dict) and data.get("result") == 'error':
        raise RuntimeError(
            "This resource requires 'view' access for idSite = %d" % (idSite))

    return data
