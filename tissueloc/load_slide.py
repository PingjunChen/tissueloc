import openslide
from PIL import Image
import numpy as np

def select_slide_level(slide_path, max_size=2048):
    """Find the slide level to perform tissue localization

    Parameters
    ----------
    slide_path : str
        Path to slide image file.
    max_size : int
        Max height and width for the size of slide with selected level.

    Returns
    -------
    level : int
        The index of the selected level.
    d_factor: int
        The downsampling factor of selected level compared to level 0.

    Notes
    -----
    The slide should have hierarchical storage structure.

    Examples
    --------
    >>> slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    >>> max_size = 3096
    >>> s_level, d_factor = select_slide_level(slide_path, max_size)
    """

    slide_head = openslide.open_slide(slide_path)
    level_dims = slide_head.level_dimensions
    d_factors = slide_head.level_downsamples

    select_level = len(level_dims) - 1
    for ind in np.arange(len(level_dims)):
        cur_w, cur_h = level_dims[ind]
        if cur_w < max_size and cur_h < max_size:
            select_level = ind
            break

    d_factor = int(d_factors[select_level])

    return select_level, d_factor


def load_slide_img(slide_path, level=0):
    """Load slide image with specific level

    Parameters
    ----------
    slide_path : str
        Path to slide image file.
    level : int
        Slide level to load.

    Returns
    -------
    np.ndarray
        A numpy array with RGB three channels.

    Notes
    -----
    Whole slide image can have more than 100,000 pixels in width or height,
    small level can be very big image.

    Examples
    --------
    >>> slide_path = "../data/SoftTissue/TCGA-PC-A5DO-01Z-00-DX1.9C3629E6-12D2-428C-A2BA-B9EB312E82F6.svs"
    >>> level = 3
    >>> slide_img = load_slide_img(slide_path, level)
    """

    slide_head = openslide.open_slide(slide_path)
    img_size = slide_head.level_dimensions[level]
    slide_img = slide_head.read_region((0, 0), level, img_size)
    if isinstance(slide_img, Image.Image):
        slide_img = np.asarray(slide_img)
    if slide_img.shape[2] == 4:
        slide_img = slide_img[:, :, :-1]
    return slide_img
