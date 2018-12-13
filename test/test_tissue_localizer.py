# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, os.path.join(PRJ_PATH, "src"))


def test_rgb2gray():
    from select_level import select_slide_level
    from load_svs import load_svs_img
    from locate_tissue import rgb2gray, thresh_slide, fill_tissue_holes
    from locate_tissue import remove_small_tissue, find_tissue_cnts
    slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    max_size = 2048
    s_level = select_slide_level(slide_path, max_size)
    slide_img = load_svs_img(slide_path, s_level)
    gray_img = rgb2gray(slide_img)
    thresh_val = 0.8
    bw_img = thresh_slide(gray_img, thresh_val)
    bw_fill = fill_tissue_holes(bw_img)
    min_size = 10000
    bw_remove = remove_small_tissue(bw_fill, min_size)
    cnts = find_tissue_cnts(bw_remove)

    slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
    cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 5)

    # import pdb; pdb.set_trace()
    plt.imshow(slide_img)
    plt.axis('off')
    plt.show()
