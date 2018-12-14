# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as misc
import cv2
import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, os.path.join(PRJ_PATH, "tissueloc"))
from load_slide import select_slide_level, load_slide_img
from locate_tissue import rgb2gray, thresh_slide, fill_tissue_holes
from locate_tissue import remove_small_tissue, find_tissue_cnts
from locate_tissue import locate_tissue_cnts



def test_locate_tissue_seperately():
    slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
    max_size = 2048
    s_level, d_factor = select_slide_level(slide_path, max_size)
    slide_img = load_slide_img(slide_path, s_level)
    gray_img = rgb2gray(slide_img)
    thresh_val = 0.8
    bw_img = thresh_slide(gray_img, thresh_val)
    bw_fill = fill_tissue_holes(bw_img)
    min_size = 10000
    bw_remove = remove_small_tissue(bw_fill, min_size)
    cnts = find_tissue_cnts(bw_remove)

    # misc.imsave('ori_slide.png', slide_img)
    slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
    cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 9)
    # misc.imsave('cnt_slide.png', slide_img)
    # import pdb; pdb.set_trace()
    # plt.imshow(slide_img)
    # plt.axis('off')
    # plt.show()


def test_locate_tissue():
    slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
    # locate tissue contours with default parameters
    cnts, d_factor = locate_tissue_cnts(slide_path,
                                        max_img_size=2048,
                                        smooth_sigma=13,
                                        thresh_val=0.80,
                                        min_tissue_size=10000)
    print("Downsampling fator is: {}".format(d_factor))
    print("There are {} contours in the slide.".format(len(cnts)))
