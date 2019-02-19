# -*- coding: utf-8 -*-

import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage import filters, img_as_ubyte
from skimage.morphology import remove_small_objects
import cv2

from .load_slide import select_slide_level, load_slide_img


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
    thresh_val: float
        Thresholding value.
    smooth_sigma: int
        Gaussian smoothing sigma.
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
    min_size: int
        Minimum tissue area.
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

    return cnts


def locate_tissue_cnts(slide_path,
                       max_img_size=2048,
                       smooth_sigma=13,
                       thresh_val = 0.80,
                       min_tissue_size=10000):
    """ Locate tissue contours of whole slide image
    Parameters
    ----------
    slide_path : valid slide path
        The slide to locate the tissue.
    max_img_size: int
        Max height and width for the size of slide with selected level.
    smooth_sigma: int
        Gaussian smoothing sigma.
    thresh_val: float
        Thresholding value.
    min_tissue_size: int
        Minimum tissue area.
    Returns
    -------
    cnts: list
        List of all contours coordinates of tissues.
    d_factor: int
        Downsampling factor of selected level compared to level 0
    """
    # Step 1: Select the proper level
    s_level, d_factor = select_slide_level(slide_path, max_img_size)
    # Step 2: Load Slide image with selected level
    slide_img = load_slide_img(slide_path, s_level)
    # Step 3: Convert color image to gray
    gray_img = rgb2gray(slide_img)
    # Step 4: Smooth and Binarize
    bw_img = thresh_slide(gray_img, thresh_val, sigma=smooth_sigma)
    # Step 5: Fill tissue holes
    bw_fill = fill_tissue_holes(bw_img)
    # Step 6: Remove small tissues
    bw_remove = remove_small_tissue(bw_fill, min_tissue_size)
    # Step 7: Locate tissue regions
    cnts = find_tissue_cnts(bw_remove)

    # slide_img = np.ascontiguousarray(slide_img, dtype=np.uint8)
    # cv2.drawContours(slide_img, cnts, -1, (0, 255, 0), 5)

    return cnts, d_factor
