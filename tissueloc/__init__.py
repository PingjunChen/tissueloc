# -*- coding: utf-8 -*-

import os, sys

__all__ = ["PKG_DIR", "__version__"]

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
__version__ = "2.1.0"

from .load_slide import *
from .locate_tissue import *
