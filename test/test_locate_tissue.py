# -*- coding: utf-8 -*-

import os, sys
import shutil
import numpy as np
import scipy.misc as misc
import cv2

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

# from tissueloc.load_slide import select_slide_level
from tissueloc.load_slide import load_slide_img
from tissueloc.locate_tissue import rgb2gray, thresh_slide, fill_tissue_holes
from tissueloc.locate_tissue import remove_small_tissue, find_tissue_cnts
# from tissueloc.locate_tissue import locate_tissue_cnts



def test_gen_intermediate_files():
    img_path = "./data/Imgs/20181218042458.jpg"
    output_dir = "./data/Output/20181218042458"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Step 2: Load Slide image with selected level
    slide_img = misc.imread(img_path)
    misc.imsave(os.path.join(output_dir, "ori.png"), slide_img)
    # Step 3: Convert color image to gray
    gray_img = rgb2gray(slide_img)
    misc.imsave(os.path.join(output_dir, "gray.png"), gray_img)
    # Step 4: Smooth and Binarize
    thresh_val = 0.8
    bw_img = thresh_slide(gray_img, thresh_val=thresh_val, sigma=5)
    misc.imsave(os.path.join(output_dir, "bw.png"), (bw_img*255.0).astype(np.uint8))
    # Step 5: Fill tissue holes
    bw_fill = fill_tissue_holes(bw_img)
    misc.imsave(os.path.join(output_dir, "fill.png"), (bw_fill*255.0).astype(np.uint8))
    # Step 6: Remove small tissues
    min_size = 10000
    bw_remove = remove_small_tissue(bw_fill, min_size)
    misc.imsave(os.path.join(output_dir, "remove.png"), (bw_remove*255.0).astype(np.uint8))
    # Step 7: Locate tissue regions
    cnts = find_tissue_cnts(bw_remove)
    slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
    cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 9)
    misc.imsave(os.path.join(output_dir, 'cnt.png'), slide_img)

# def test_locate_tissue_seperately():
#     slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
#     max_size = 2048
#     # Step 1: Select the proper level
#     s_level, d_factor = select_slide_level(slide_path, max_size)
#     # Step 2: Load Slide image with selected level
#     slide_img = load_slide_img(slide_path, s_level)
#     # misc.imsave('ori.png', slide_img)
#     # Step 3: Convert color image to gray
#     gray_img = rgb2gray(slide_img)
#     # misc.imsave("gray.png", gray_img)
#     # Step 4: Smooth and Binarize
#     thresh_val = 0.8
#     bw_img = thresh_slide(gray_img, thresh_val)
#     # misc.imsave("bw.png", (bw_img*255.0).astype(np.uint8))
#     # Step 5: Fill tissue holes
#     bw_fill = fill_tissue_holes(bw_img)
#     # misc.imsave("fill.png", (bw_fill*255.0).astype(np.uint8))
#     # Step 6: Remove small tissues
#     min_size = 10000
#     bw_remove = remove_small_tissue(bw_fill, min_size)
#     # misc.imsave("remove.png", (bw_remove*255.0).astype(np.uint8))
#     # Step 7: Locate tissue regions
#     cnts = find_tissue_cnts(bw_remove)
#     # slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
#     # cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 9)
#     # misc.imsave('cnt.png', slide_img)


# def test_locate_tissue():
#     slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
#     # locate tissue contours with default parameters
#     cnts, d_factor = locate_tissue_cnts(slide_path,
#                                         max_img_size=2048,
#                                         smooth_sigma=13,
#                                         thresh_val=0.80,
#                                         min_tissue_size=10000)
#     print("Downsampling fator is: {}".format(d_factor))
#     print("There are {} contours in the slide.".format(len(cnts)))
