#!/usr/bin/env python

import gimpfu


def my_python_function(timg, tdrawable):
    first_layer = timg.layers[0]
    first_layer.name = "my first action"


register(
    proc_name=("my_gimp_name"),
    blurb=("short description"),
    help=("long description"),
    author=("author"),
    copyright=("owner"),
    date=("year"),
    label=(""),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "")
    ]
    results=[]
    function=(unsere func die wir noch machen),
    menu=("<Image>/Filters/YourChoice")
    domain=("gimp20-python", gimp.locale_directory)
)
main()


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
