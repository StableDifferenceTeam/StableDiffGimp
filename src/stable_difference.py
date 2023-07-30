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

        # for each obj in cmd_module_filenames[]:
        for cmd_module_filename in cmd_module_filenames:
            for _, obj in inspect.getmembers(import_module(cmd_module_filename), is_cmd):
                # if obj is a valid command and not already registered
                if obj.__name__ not in registered_cmds:
                    print("Registering command: " + obj.__name__)

                    # set command_runner to run_sd_command if StableDiffusionCommand, else run_command
                    if 'StableDiffusionCommand' in [cls.__name__ for cls in inspect.getmro(obj)]:
                        obj.command_runner = sdiff.run_stable_diffusion_command
                    # else is eg. the Settings Command
                    else:
                        obj.command_runner = sdiff.run_command

                    # register command and open gtk dialog
                    gimpfu.register(*obj.metadata, function=obj._open_gtk_options)

                    # add command to registered_cmds[] to avoid double registration (just precaution)
                    registered_cmds.append(obj.__name__)

    ssl._create_default_https_context = ssl._create_unverified_context

    gimpfu.main()