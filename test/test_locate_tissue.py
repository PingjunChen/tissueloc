# -*- coding: utf-8 -*-

import os, sys
import shutil
import numpy as np
from skimage import io, color
import cv2

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
PRJ_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

# from tissueloc.load_slide import select_slide_level
from tissueloc.load_slide import load_slide_img
from tissueloc.locate_tissue import thresh_slide, fill_tissue_holes
from tissueloc.locate_tissue import remove_small_tissue, find_tissue_cnts

def test_gen_intermediate_files():
    img_path = os.path.join(TEST_PATH, "data/Imgs/20181218042458.jpg")
    output_dir = os.path.join(TEST_PATH, "data/Output/20181218042458")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Step 2: Load Slide image with selected level
    slide_img = io.imread(img_path)
    io.imsave(os.path.join(output_dir, "ori.png"), slide_img)
    # Step 3: Convert color image to gray
    gray_img = color.rgb2gray(slide_img)
    io.imsave(os.path.join(output_dir, "gray.png"), gray_img)
    # Step 4: Smooth and Binarize
    thresh_val = 0.8
    bw_img = thresh_slide(gray_img, thresh_val=thresh_val, sigma=5)
    io.imsave(os.path.join(output_dir, "bw.png"), (bw_img*255.0).astype(np.uint8))
    # Step 5: Fill tissue holes
    bw_fill = fill_tissue_holes(bw_img)
    io.imsave(os.path.join(output_dir, "fill.png"), (bw_fill*255.0).astype(np.uint8))
    # Step 6: Remove small tissues
    min_size = 10000
    bw_remove = remove_small_tissue(bw_fill, min_size)
    io.imsave(os.path.join(output_dir, "remove.png"), (bw_remove*255.0).astype(np.uint8))
    # Step 7: Locate tissue regions
    cnts = find_tissue_cnts(bw_remove)
    slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
    cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 9)
    io.imsave(os.path.join(output_dir, 'cnt.png'), slide_img)

# def test_locate_tissue_seperately():
#     slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
#     max_size = 2048
#     # Step 1: Select the proper level
#     s_level, d_factor = select_slide_level(slide_path, max_size)
#     # Step 2: Load Slide image with selected level
#     slide_img = load_slide_img(slide_path, s_level)
#     # io.imsave('ori.png', slide_img)
#     # Step 3: Convert color image to gray
#     gray_img = rgb2gray(slide_img)
#     # io.imsave("gray.png", gray_img)
#     # Step 4: Smooth and Binarize
#     thresh_val = 0.8
#     bw_img = thresh_slide(gray_img, thresh_val)
#     # io.imsave("bw.png", (bw_img*255.0).astype(np.uint8))
#     # Step 5: Fill tissue holes
#     bw_fill = fill_tissue_holes(bw_img)
#     # io.imsave("fill.png", (bw_fill*255.0).astype(np.uint8))
#     # Step 6: Remove small tissues
#     min_size = 10000
#     bw_remove = remove_small_tissue(bw_fill, min_size)
#     # io.imsave("remove.png", (bw_remove*255.0).astype(np.uint8))
#     # Step 7: Locate tissue regions
#     cnts = find_tissue_cnts(bw_remove)
#     # slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
#     # cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 9)
#     # io.imsave('cnt.png', slide_img)


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
