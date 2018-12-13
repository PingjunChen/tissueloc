# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, os.path.join(PRJ_PATH, "src"))


def test_load_svs_img():
    from select_level import select_slide_level
    from load_svs import load_svs_img
    slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    max_size = 2048
    s_level = select_slide_level(slide_path, max_size)
    slide_img = load_svs_img(slide_path, s_level)

    assert isinstance(slide_img, np.ndarray)
    img_channel = slide_img.shape[2]
    assert img_channel == 3, "Slide channel is {}".format(img_channel)
