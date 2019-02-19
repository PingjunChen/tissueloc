# -*- coding: utf-8 -*-

import os, sys
# import numpy as np
# import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, PRJ_PATH)
# from tissueloc.load_slide import select_slide_level
# from tissueloc.load_slide import load_slide_img


# def test_select_slide_level():
#     slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
#     max_size = 2048
#     s_level, d_factor = select_slide_level(slide_path, max_size)
#     print("Selected level is: {}".format(s_level))
#     print("Downsampling factor is: {}".format(d_factor))
#     assert s_level >=0 and s_level <=10
#     assert d_factor >= 1
#
#
# def test_load_slide_img():
#     slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
#     max_size = 2048
#     s_level, _ = select_slide_level(slide_path, max_size)
#     slide_img = load_slide_img(slide_path, s_level)
#
#     assert isinstance(slide_img, np.ndarray)
#     img_channel = slide_img.shape[2]
#     assert img_channel == 3, "Slide channel is {}".format(img_channel)
