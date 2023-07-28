#! /usr/bin/env python2

from glob import glob
import gimpfu
import os
import sys
from importlib import import_module
import inspect
import ssl
import json

# Fix relative imports in Windows
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, path)
import stabledifference as sdiff

# def center_elements(image, drawable):
#    pass
#   # Add your code to center the visible layers here
#   # pass
#
#
# This is the plugin registration function
# register(
#    "center",
#    "Center visible layers",
#    "Center elements",
#    "Poop Head",
#    "Poop Head",
#    "2023",
#    "<Image>/StableDifference/Center_Elements",
#    "*",
#    [],
#    [],
#    center_elements
# )
#
# main()

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
if __name__ == "__main__":

    # def is_cmd() simple function to check if we are in cmd or not (just precaution)
    def is_cmd(obj):
        return inspect.isclass(obj) and obj.__name__ not in ['StableDifferenceCommand', 'StableDiffusionCommand'] \
            and 'StableDifferenceCommand' in [cls.__name__ for cls in inspect.getmro(obj)]

    # get all files from folder .stabledifference\commands into cmd_module_locations[]
    cmd_module_locations = [["stabledifference", "commands"]]

    # initialize empty list with registered commands registered_cmds[] to avoid double registration (just precaution)
    # if a command is registered, it actually shows up in gimp
    registered_cmds = []

    # for each obj in cmd_module_locations[]:
    for cmd_module_location in cmd_module_locations:
        # get all filenames from command folder into cmd_module_filenames[]
        # for example: cmd_module_filenames[x] == "stabledifference.commands.text-to-image.py"
        cmd_module_filenames = [".".join(cmd_module_location) + "." + os.path.splitext(os.path.basename(c))[
            0] for c in glob(os.path.join(os.path.dirname(__file__), *(cmd_module_location + ["*.py"])))]

        # for each filename in cmd_module_filenames[]:
        for cmd_module_filename in cmd_module_filenames:
            for _, obj in inspect.getmembers(import_module(cmd_module_filename), is_cmd):
                # if obj is a valid command and not already registered
                if obj.__name__ not in registered_cmds:
                    print("Registering command: " + obj.__name__)

                    # set command_runner to run_sd_command if StableDiffusionCommand, else run_command
                    if 'StableDiffusionCommand' in [cls.__name__ for cls in inspect.getmro(obj)]:
                        obj.command_runner = sdiff.run_stable_diffusion_command
                    # else is eg. the Preferences Command
                    else:
                        obj.command_runner = sdiff.run_command

                    # register command
                    gimpfu.register(*obj.metadata, function=obj._show_advanced_options)

                    # add command to registered_cmds[] to avoid double registration (just precaution)
                    registered_cmds.append(obj.__name__)

    ssl._create_default_https_context = ssl._create_unverified_context

    if not os.path.isfile('settings.json'):
       print("settings.json does not exist")
       with open('settings.json', 'w') as f:
            json.dump({"api_base_url": sdiff.constants.DEFAULT_API_URL}, f) 

    gimpfu.main()

#  if obj not in registered_cmds[] and obj.is_cmd():
#   run command via command_runner
#   obj.register()
#   registered_cmds.append(obj)

# In stable Boy stable diffusion and other commands are differentiated,
# but thats stuff we gotta worry about later i'd say.
# other commands include setting Preferences, etc.
