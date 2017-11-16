#! /usr/bin/env python

"""This module provides a simple task scheduler

Each job is contained in a bash file

"""
from __future__ import division, print_function

from cluster import bwnemo, hel


def execute(jobs, clustername, parameters):
    if clustername == 'BWnemo':
        bwnemo.execute(jobs, **parameters)
    elif clustername == 'hel':
        hel.execute(jobs, **parameters)
    else:
        raise NotImplementedError()


def check_status():
    raise NotImplementedError()
