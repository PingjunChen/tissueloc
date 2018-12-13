# -*- coding: utf-8 -*-

import os, sys
import openslide
import numpy as np


def select_slide_level(slide_path, max_size=2048):
    """Find the slide level to perform tissue localization
    Parameters
    ----------
    slide_path : valid slide path
        The slide to process.
    max_size : int
        Max height and width for the size of slide with selected level
    Returns
    -------
    level : int
        Selected level.
    Notes
    -----
    The slide should have hierarchical storage structure.
    Examples
    --------
    >>> from select_level import select_slide_level
    >>> slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    >>> max_size = 3096
    >>> s_level = select_slide_level(slide_path, max_size)
    """

    slide_head = openslide.open_slide(slide_path)
    level_dims = slide_head.level_dimensions
    assert len(level_dims) > 1, "This slide doesnot have mutliple levels"
    select_level = len(level_dims) - 1
    for ind in np.arange(len(level_dims)):
        cur_w, cur_h = level_dims[ind]
        if cur_w < max_size and cur_h < max_size:
            select_level = ind
            break

    return select_level
