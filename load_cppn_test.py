"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""

from make_cppn import load_cppn
from make_image import make_image

CPPN_DIRECTORY = "cppns/37"

cppn = load_cppn(CPPN_DIRECTORY)
image = make_image(cppn, 64, 64, image_directory=None, save=False)
image.show()