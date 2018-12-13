# -*- coding: utf-8 -*-

import os, sys
import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, os.path.join(PRJ_PATH, "src"))

def test_select_slide_level():
    from select_level import select_slide_level
    slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    max_size = 2048
    s_level = select_slide_level(slide_path, max_size)
    print("Selected level is: {}".format(s_level))
    assert s_level >=0 and s_level <=8
