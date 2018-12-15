Load Slide
========

select_slide_level
--------
::

def select_slide_level(slide_path, max_size=2048):
    """Find the slide level to perform tissue localization

    Parameters:
    slide_path : valid slide path
        The slide to process.
    max_size : int
        Max height and width for the size of slide with selected level

    Returns:
    level : int
        Selected level.
    d_factor: int
        Downsampling factor of selected level compared to level 0

    Notes: 
    The slide should have hierarchical storage structure.

    """


load_slide_img
--------
::

def load_slide_img(slide_path, level=0):
    """Load slide image with specific level

    Parameters:
    slide_path : valid slide path
        The slide to load.
    level : int
        Slide level to load.
    
    Returns:
    slide_img : np.array
        Numpy matrix with RGB three channels.

    Notes:

    Whole slide image can have more than 100,000 pixels in width or height,
    small level can be very big image.

    """