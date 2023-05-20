#! /usr/bin/env python2
from gimpfu import *


def center_elements(image, drawable):
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
    center_elements
)

main()

#!/usr/bin/env python

#from gimpfu import *


# def my_python_function(timg, tdrawable):
#    first_layer = timg.layers[0]
#    first_layer.name = "my first action"


# register(
#    proc_name=("my_gimp_name"),
#    blurb=("short description"),
#    help=("long description"),
#    author=("author"),
#    copyright=("owner"),
#    date=("year"),
#    label=(""),
#    imagetypes=("*"),
#    params=[
#        (PF_IMAGE, "")
#    ]
#    results=[]
#    function=(unsere func die wir noch machen),
#    menu=("<Image>/Filters/YourChoice")
#    domain=("gimp20-python", gimp.locale_directory),
#
# )
# main()


# Workflow for Main (like in the main of stableboy):

# def is_cmd() simple function to check if we are in cmd or not (just precaution)

# get all files from folder .stableboy\commands into cmd_module_locations[]

# initialize empty list with registered commands registered_cmds[] to avoid double registration (just precaution)

# for each obj in cmd_module_locations[]:
#  if obj not in registered_cmds[] and obj.is_cmd():
#   run command via command_runner
#   obj.register()
#   registered_cmds.append(obj)


# In stable Boy stable diffusion and other commands are differentiated,
# but thats stuff we gotta worry about later i'd say.
# other commands include setting Preferences, etc.
