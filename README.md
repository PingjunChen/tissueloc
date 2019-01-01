tissueloc
========
[![Build Status](https://travis-ci.org/PingjunChen/tissueloc.svg?branch=master)](https://travis-ci.org/PingjunChen/tissueloc)
[![Documentation Status](https://readthedocs.org/projects/tissueloc/badge/?version=latest)](https://tissueloc.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/tissueloc.svg)](https://badge.fury.io/py/tissueloc)
![](https://img.shields.io/github/license/PingjunChen/tissueloc.svg)

## Localize the tissue regions in whole slide pathology images

<img src="tissuelocDemo.png" width="800" height="320" alt="Banner">

## Installation
1. Install [OpenSlide](https://openslide.org/download/).
```
$ apt-get install openslide-tools
```
2. Installing Python dependencies.
```
$ pip install opencv-python
$ pip install scikit-image
$ pip install openslide-python
```
3. Install [tissueloc](https://pypi.org/project/tissueloc/).
```
$ pip install tissueloc
```

## Usage
```
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
```

### Example
Testing slide can be downloaded from [Figshare](https://figshare.com/articles/Demo_Whole_Slide_Images/7532978).
```
import tissueloc as tl
slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
# locate tissue contours with default parameters
cnts, d_factor = locate_tissue_cnts(slide_path,
                                    max_img_size=2048,
                                    smooth_sigma=13,
                                    thresh_val=0.80,
                                    min_tissue_size=10000)
```

### Procedures
```
import tissueloc as tl
# Step 1: Select the proper level
slide_path = "../data/SoftTissue/TCGA-B9EB312E82F6.svs"
max_img_size = 2048
s_level, d_factor = tl.select_slide_level(slide_path, max_img_size)
# Step 2: Load Slide image with selected level
slide_img = tl.load_slide_img(slide_path, s_level)
# Step 3: Convert color image to gray
gray_img = tl.rgb2gray(slide_img)
# Step 4: Smooth and Binarize
thresh_val = 0.8
smooth_sigma = 13
bw_img = tl.thresh_slide(gray_img, thresh_val, sigma=smooth_sigma)
# Step 5: Fill tissue holes
bw_fill = tl.fill_tissue_holes(bw_img)
# Step 6: Remove small tissues
min_tissue_size = 10000
bw_remove = tl.remove_small_tissue(bw_fill, min_tissue_size)
# Step 7: Locate tissue regions
cnts = tl.find_tissue_cnts(bw_remove)
```


## Documentation
Hosted in [https://tissueloc.readthedocs.io](https://tissueloc.readthedocs.io), powered by [readthedocs](https://readthedocs.org) and [Sphinx](http://www.sphinx-doc.org).

## License
[tissueloc](https://github.com/PingjunChen/tissueloc) is free software made available under the MIT License. For details see the [LICENSE](LICENSE) file.

## Contributors
See the [AUTHORS.md](AUTHORS.md) file for a complete list of contributors to the project.


## Contributing
``tissueloc`` is an  open source project and anyone is welcome to contribute. An easy way to get started is by suggesting a new enhancement on the [Issues](https://github.com/PingjunChen/tissueloc/issues). If you have found a bug, then either report this through [Issues](https://github.com/PingjunChen/tissueloc/issues), or even better, make a fork of the repository, fix the bug and then create a [Pull Requests](https://github.com/PingjunChen/tissueloc/pulls) to get the fix into the master branch.

We would like to test this package on more diversified digital slides. Slides (low level images would be better) and their corresponding results are also very welcome as [Pull Requests](https://github.com/PingjunChen/tissueloc/pulls).
