#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-10 13:08:30
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-10 13:08:45

from __future__ import unicode_literals


def test_version_check():
    from clicktrack import _version

    ######################################################
    # THIS NEEDS TO BE UPDATED EVERY TIME THE MAIN PACKAGE
    # VERSION IS UPDATED!!!
    ######################################################
    # eg, expected
    # version_info = ('0', '0', '1')
    # __version__ = '.'.join(version_info[0:3])
    _v = '0.0.1'

    if _version.__version__ != _v:
        raise SystemError('SYNC VERSION in tests/test_clicktrack.py')


# MAKE THIS SO IT ONLY EVER GETS RUN ONCE PER "SESSION"
def test_global_import():
    import clicktrack
