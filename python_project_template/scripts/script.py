#!/usr/bin/env python

import sys
from os.path import dirname, realpath

sys.path.insert(0, dirname(dirname(realpath(__file__))))

import resources.useful_resource as r


if __name__ == '__main__':
    r.useful_function()

