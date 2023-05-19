#! /usr/bin/env python

import os
import sys
import gimpfu

# main function to be called by GIMP


# Just a dummy function to test the plugin, it does nothing
# the plugin should have a button next to file, edit, select, view, etc.
# and it should be called "Hello World"

if __name__ == "__main__":

    def plugin_main():
        pass

    # This is the plugin registration function
    gimpfu.register(
        "python_fu_hello_world",
        "Hello World",
        "Hello World",
        "Your Name",
        "Your Name",
        "2019",
        "<Image>/Filters/Artistic/Hello World",
        "",  # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
        "",
        [],  # type of drawable it works on (IMAGE, VISIBLE_LAYERS, etc...)
        [],  # other parameters
        plugin_main)  # callback function

    gimpfu.main()
