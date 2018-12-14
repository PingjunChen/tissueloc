# -*- coding: utf-8 -*-

import os, sys

__all__ = ["SRC_DIR", "DATA_DIR"]

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(os.path.dirname(SRC_DIR), 'data')

from .load_slide import *
from .locate_tissue import *
