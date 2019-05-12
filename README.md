tissueloc: Whole slide digital pathology image tissue localization
=============
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2f1d165f709e43c4bc6d1d3a6563418e)](https://app.codacy.com/app/PingjunChen/tissueloc?utm_source=github.com&utm_medium=referral&utm_content=PingjunChen/tissueloc&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/PingjunChen/tissueloc.svg?branch=master)](https://travis-ci.org/PingjunChen/tissueloc)
[![Documentation Status](https://readthedocs.org/projects/tissueloc/badge/?version=latest)](https://tissueloc.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/tissueloc.svg)](https://badge.fury.io/py/tissueloc)
[![DOI](http://joss.theoj.org/papers/10.21105/joss.01148/status.svg)](https://doi.org/10.21105/joss.01148)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/PingjunChen)
![](https://img.shields.io/github/stars/PingjunChen/tissueloc.svg)
<img src="./docs/media/tissuelocDemo.png" width="800" height="320" alt="Banner">

Installation
-------------
1. Install [OpenSlide](https://openslide.org/download/).
```
$ sudo apt-get install openslide-tools
```
2. Installing Python dependencies.
```
$ pip install opencv-python
$ pip install scikit-image
$ pip install openslide-python
```
3. Install [tissueloc](https://pypi.org/project/tissueloc/).
```
$ pip install tissueloc==2.0.1
```

Usage example
-------------
#### Interface
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

#### Demo
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

Documentation
-------------
Hosted in [https://tissueloc.readthedocs.io](https://tissueloc.readthedocs.io), powered by [readthedocs](https://readthedocs.org) and [Sphinx](http://www.sphinx-doc.org).

Contributing
-------------
``tissueloc`` is an  open source project and anyone is welcome to contribute. An easy way to get started is by suggesting a new enhancement on the [Issues](https://github.com/PingjunChen/tissueloc/issues). If you have found a bug, then either report this through [Issues](https://github.com/PingjunChen/tissueloc/issues), or even better, make a fork of the repository, fix the bug and then create a [Pull Requests](https://github.com/PingjunChen/tissueloc/pulls) to get the fix into the master branch.

We would like to test this package on more diversified digital slides. Slides (low level images would be better) and their corresponding results are also very welcome as [Pull Requests](https://github.com/PingjunChen/tissueloc/pulls).

License
-------------
[tissueloc](https://github.com/PingjunChen/tissueloc) is free software made available under the MIT License. For details see the [LICENSE](LICENSE) file.

Contributors
-------------
See the [AUTHORS.md](AUTHORS.md) file for a complete list of contributors to the project.

Citing
-------------
``tissueloc`` is published in the Journal of Open Source Software - please cite if it's useful for your research:
```
@article{chen2019tissueloc,
  author    = {Pingjun Chen and Lin Yang},
  title     = {tissueloc: Whole slide digital pathology image tissue localization},
  journal   = {J. Open Source Software},
  volume    = {4},
  number    = {33},
  pages     = {1148},
  year      = {2019},
  url       = {https://doi.org/10.21105/joss.01148},
  doi       = {10.21105/joss.01148}
}
```
