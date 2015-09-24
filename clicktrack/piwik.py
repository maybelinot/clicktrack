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

# Config for this module is under 'piwik'; eg
# cat ~/.clicktrack (YAML)
# piwik
#     domain: ...
#     idSite: ...
#     ...
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
        _config = yaml.load(_) or {}
        conf = _config.get('piwik') or {}

    domain = domain or conf.get('domain')
    conf['idSite'] = idSite or conf.get('idSite')
    if domain is None:
        raise TypeError("Domain should be provided")
    if conf['idSite'] is None:
        raise TypeError("idSite should be provided")
    conf['period'] = period or conf.get('period')
    # expected as str YYYY-MM-DD,YYY-MM-DD
    conf['date'] = date or conf.get('date', '{},{}'.format(YESTERDAY, TODAY))
    conf['expanded'] = int(expanded or conf.get('expanded', 1))
    conf['filter_limit'] = int(filter_limit or conf.get('filter_limit', -1))
    conf['filter_column'] = filter_column or conf.get('filter_column', 'label')
    conf['filter_pattern'] = filter_pattern or conf.get('filter_pattern')
    # these should come in already as csv string
    # eg, 'label, nb_hits, nb_visits'
    conf['showColumns'] = showColumns or conf.get('showColumns')
    conf['hideColumns'] = hideColumns or conf.get('hideColumns')

    '''list all available columns in the documentation strings'''
    payload = {
        'module': 'API',
        'method': 'Actions.getPageUrls',
        'format': format or conf.get('format'),
        'translateColumnNames': True,
        'language': 'en',
    }
    payload.update(conf)

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
