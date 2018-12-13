# -*- coding: utf-8 -*-

import os, sys
import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage import filters, img_as_ubyte
from skimage.morphology import remove_small_objects

import cv2

def rgb2gray(img):
    """Convert RGB image to gray space.
    Parameters
    ----------
    img : np.array
        RGB image with 3 channels.
    Returns
    -------
    gray: np.array
        Gray image
    """
    gray = np.dot(img, [0.299, 0.587, 0.114])

    return gray


def thresh_slide(gray, thresh_val, sigma=13):
    """ Threshold gray image to binary image
    Parameters
    ----------
    gray : np.array
        2D gray image.
    Returns
    -------
    bw_img: np.array
        Binary image
    """

    # Smooth
    smooth = filters.gaussian(gray, sigma=sigma)
    smooth /= np.amax(smooth)
    # Threshold
    bw_img = smooth < thresh_val

    return bw_img


def fill_tissue_holes(bw_img):
    """ Filling holes in tissue image
    Parameters
    ----------
    bw_img : np.array
        2D binary image.
    Returns
    -------
    bw_fill: np.array
        Binary image with no holes
    """

    # Fill holes
    bw_fill = binary_fill_holes(bw_img)

    return bw_fill

def remove_small_tissue(bw_img, min_size=10000):
    """ Remove small holes in tissue image
    Parameters
    ----------
    bw_img : np.array
        2D binary image.
    Returns
    -------
    bw_remove: np.array
        Binary image with small tissue regions removed
    """

    bw_remove = remove_small_objects(bw_img, min_size=min_size, connectivity=8)

    return bw_remove


def find_tissue_cnts(bw_img):
    """ Fint contours of tissues
    Parameters
    ----------
    bw_img : np.array
        2D binary image.
    Returns
    -------
    cnts: list
        List of all contours coordinates of tissues.
    """

    _, cnts, _ = cv2.findContours(img_as_ubyte(bw_img),
                                  mode=cv2.RETR_EXTERNAL,
                                  method=cv2.CHAIN_APPROX_NONE)
    # list_cnts_arr = []
    # for ele in cnts:
    #     cnt_arr = ele.squeeze().transpose()
    #     list_cnts_arr.append(cnt_arr)
    #
    # return list_cnts_arr

    return cnts
