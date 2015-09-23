#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-10 13:10:29
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-10 14:40:21

from __future__ import unicode_literals


def test_global_import():
    from clicktrack import piwik


def test_get_page_urls_failure():
    from clicktrack.piwik import get_page_urls

    domain = "http://demo.piwik.org/index.php"
    site_id = 1

    try:
        get_page_urls(domain, site_id=site_id)
    except RuntimeError:
        assert True


def test_get_page_urls():
    import datetime as dt
    import json

    import requests as rq

    from clicktrack.piwik import get_page_urls

    YESTERDAY = dt.datetime.utcnow() - dt.timedelta(1)
    TODAY = dt.date.today()
    date = (YESTERDAY, TODAY)

    domain = "http://demo.piwik.org/index.php"
    site_id = 7
    show_columns = ['label', 'nb_hits', 'nb_visits']
    hide_columns = None

    payload = {'module': 'API',
               'method': 'Actions.getPageUrls',
               'format': 'json',
               'idSite': site_id,
               'period': 'range',
               'date': '%s,%s' % tuple(d.strftime("%Y-%m-%d") for d in date),
               'expanded': int(True),
               'filter_limit': -1,
               'translateColumnNames': True,
               'language': 'en',
               'filter_column': 'label',
               'filter_pattern': None,
               'showColumns': ','.join(show_columns) if show_columns else None,
               'hideColumns': ','.join(hide_columns) if hide_columns else None}
    data = rq.get(domain,
                  params=payload,
                  verify=False).text
    data = json.loads(data)

    assert data == get_page_urls(domain, site_id=site_id,
                                 show_columns=show_columns,
                                 date=date)
