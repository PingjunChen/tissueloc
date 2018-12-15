Locate Tissue
========

locate_tissue_cnts
--------
::

def locate_tissue_cnts(slide_path,
                       max_img_size=2048,
                       smooth_sigma=13,
                       thresh_val = 0.80,
                       min_tissue_size=10000):
    """ Locate tissue contours of whole slide image

    Parameters

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

    cnts: list
        List of all contours coordinates of tissues.
    d_factor: int
        Downsampling factor of selected level compared to level 0
    """

rgb2gray
--------
::

def rgb2gray(img):
    """Convert RGB image to gray space.

    Parameters

    img : np.array
        RGB image with 3 channels.

    Returns

    gray: np.array
        Gray image
    """

thresh_slide
--------
::

def thresh_slide(gray, thresh_val, sigma=13):
    """ Threshold gray image to binary image
    
	Parameters

    gray : np.array
        2D gray image.
    thresh_val: float
        Thresholding value.
    smooth_sigma: int
        Gaussian smoothing sigma.

    Returns

    bw_img: np.array
        Binary image
    """

fill_tissue_holes
--------
::

def fill_tissue_holes(bw_img):
    """ Filling holes in tissue image

    Parameters

    bw_img : np.array
        2D binary image.

    Returns

    bw_fill: np.array
        Binary image with no holes
    """

remove_small_tissue
--------
::

def remove_small_tissue(bw_img, min_size=10000):
   """ Remove small holes in tissue image

    Parameters

    bw_img : np.array
        2D binary image.
    min_size: int
        Minimum tissue area.

    Returns

    bw_remove: np.array
        Binary image with small tissue regions removed
    """

find_tissue_cnts
--------
::

def find_tissue_cnts(bw_img):
    """ Fint contours of tissues

    Parameters

    bw_img : np.array
        2D binary image.

    Returns

    cnts: list
        List of all contours coordinates of tissues.
    """


