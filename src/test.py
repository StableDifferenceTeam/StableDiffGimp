#! /usr/bin/env python
from gimpfu import *

def test_elements(image, drawable):
    # Add your code to center the visible layers here
    pass

# This is the plugin registration function
register(
    "center",
    "Center visible layers",
    "Center elements",
    "Poop Head",
    "Poop Head",
    "2023",
    "<Image>/Functionality/Center_Elements",
    "*",
    [],
    [],
    test_elements
)

main()
