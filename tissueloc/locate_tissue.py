# -*- coding: utf-8 -*-

import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage import filters, img_as_ubyte
from skimage.morphology import remove_small_objects
import cv2

from .load_slide import select_slide_level, load_slide_img


def rgb2gray(img):
    """Convert RGB image to gray space.

    Args:
        img (np.ndarray): RGB image with 3 channels.

    Returns:
        np.ndarray: Gray image
    """
    return np.dot(img, [0.299, 0.587, 0.114])


def thresh_slide(gray, thresh_val, sigma=13):
    """ Threshold gray image to binary image.

    Args:
        gray (np.ndarray): 2D gray image.
        thresh_val (float): Thresholding value.
        smooth_sigma (int): Gaussian smoothing sigma.

    Returns:
        np.ndarray: Binary image
    """

    # Smooth
    smooth = filters.gaussian(gray, sigma=sigma)
    smooth /= np.amax(smooth)
    # Threshold
    bw_img = smooth < thresh_val

    return bw_img


def fill_tissue_holes(bw_img):
    """ Filling holes in tissue image.

    Args:
        bw_img (np.ndarray): 2D binary image.

    Returns:
        np.ndarray: Binary image with no holes
    """

    # Fill holes
    bw_fill = binary_fill_holes(bw_img)

    return bw_fill


def remove_small_tissue(bw_img, min_size=10000):
    """Remove small holes in tissue image.

    Args:
        bw_img (np.ndarray): 2D binary image.
        min_size (int): Minimum tissue area.

    Returns:
        np.ndarray: Binary image with small tissue regions removed.

    Raises:
        ValueError: If `bw_img` is not a 2D numpy array or `min_size` is not a positive integer.
    """

    if not isinstance(bw_img, np.ndarray) or bw_img.ndim != 2:
        raise ValueError("bw_img must be a 2D numpy array")

    if not isinstance(min_size, int) or min_size <= 0:
        raise ValueError("min_size must be a positive integer")

    return remove_small_objects(bw_img, min_size=min_size, connectivity=8)


def find_tissue_cnts(bw_img):
    """Find contours of tissues.

    Args:
        bw_img (np.ndarray): 2D binary image.

    Returns:
        list: List of all contours coordinates of tissues.

    Raises:
        ValueError: If `bw_img` is not a 2D numpy array.
    """
    if not isinstance(bw_img, np.ndarray) or bw_img.ndim != 2:
        raise ValueError("bw_img must be a 2D numpy array")

    _, cnts, _ = cv2.findContours(img_as_ubyte(bw_img), mode=cv2.RETR_CCOMP,
                                  method=cv2.CHAIN_APPROX_NONE)

    return cnts


def locate_tissue_cnts(slide_path,
                       max_img_size=2048,
                       smooth_sigma=13,
                       thresh_val=0.80,
                       min_tissue_size=10000):
    """Locate tissue contours of whole slide image.

    Args:
        slide_path (str): Valid slide path.
        max_img_size (int): Max height and width for the size of slide with selected level.
        smooth_sigma (int): Gaussian smoothing sigma.
        thresh_val (float): Thresholding value.
        min_tissue_size (int): Minimum tissue area.

    Returns:
        tuple: A tuple containing the list of all contours coordinates of tissues and the downsampling factor of selected level compared to level 0.

    Raises:
        ValueError: If `slide_path` is not a valid string path or any of the other input parameters are invalid.
    """
    if not isinstance(slide_path, str) or not slide_path:
        raise ValueError("slide_path must be a valid string path")

    if not isinstance(max_img_size, int) or max_img_size <= 0:
        raise ValueError("max_img_size must be a positive integer")

    if not isinstance(smooth_sigma, int) or smooth_sigma <= 0:
        raise ValueError("smooth_sigma must be a positive integer")

    if not isinstance(thresh_val, float) or thresh_val < 0 or thresh_val > 1:
        raise ValueError("thresh_val must be a float between 0 and 1")

    if not isinstance(min_tissue_size, int) or min_tissue_size <= 0:
        raise ValueError("min_tissue_size must be a positive integer")

    with select_slide_level(slide_path, max_img_size) as (s_level, d_factor), \
         load_slide_img(slide_path, s_level) as slide_img:
        # Convert color image to gray
        gray_img = rgb2gray(slide_img)
        # Smooth and Binarize
        bw_img = thresh_slide(gray_img, thresh_val, sigma=smooth_sigma)
        # Fill tissue holes
        bw_fill = fill_tissue_holes(bw_img)
        # Remove small tissues
        bw_remove = remove_small_tissue(bw_fill, min_tissue_size)
        # Locate tissue regions
        cnts = find_tissue_cnts(bw_remove)

    return cnts, d_factor
