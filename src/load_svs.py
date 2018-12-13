# -*- coding: utf-8 -*-

import os, sys
import openslide
from PIL import Image
import numpy as np

def load_svs_img(slide_path, level=0):
    """Load slide image with specific level
    Parameters
    ----------
    slide_path : valid slide path
        The slide to load.
    level : int
        Slide level to load.
    Returns
    -------
    slide_img : np.array
        Numpy matrix with RGB three channels.
    Notes
    -----
    Whole slide image can have more than 100,000 pixels in width or height,
    small level can be very big image.
    Examples
    --------
    >>> from load_svs import load_svs_img
    >>> slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    >>> level = 3
    >>> slide_img = load_svs_img(slide_path, level)
    """

    slide_head = openslide.open_slide(slide_path)
    img_size = slide_head.level_dimensions[level]
    slide_img = slide_head.read_region((0, 0), level, img_size)
    if isinstance(slide_img, Image.Image):
        slide_img = im = np.asarray(slide_img)
    if slide_img.shape[2] == 4:
        slide_img = slide_img[:, :, :-1]
    return slide_img
