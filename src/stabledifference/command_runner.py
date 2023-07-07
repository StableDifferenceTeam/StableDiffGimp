# Workflow for command runner:


# for basic commands like preferences, run_command(cmd) is called,
# which calls the command's run() and join() methods.

# ----------------------------------------------------------------

# for stable diffusion, run_sd_command(cmd) is called
# cmd.start() and do Progress updates (just aesthetics)
# if cmd.status == "DONE":
#   cmd.join()
#   unpack, create layers open images, etc.
#   just put the stuff in the right place


# ----------------------------------------------------------------

import gtk
from gimpfu import *
import gimp_functions
from .config import Config as config

# Basic Command runner, no progress updates


def run_command(cmd):
    cmd.start()
    cmd.join()
    # gimp.progress_update(1.0)


def run_stable_diffusion_command(cmd):
    try:
        cmd.start()
        # TODO add some progress updates here (aesthetics)

        # wait for the command to complete
        while cmd.status != "DONE" and cmd.status != "ERROR":
            pass
        if cmd.status == "ERROR":
            pass
        else:
            cmd.join()
            cmd.img.undo_group_start()
            apply_inpainting_mask = hasattr(
                cmd, 'apply_inpainting_mask') and cmd.apply_inpainting_mask
            gimp_functions.create_layers(
                cmd.img, cmd.layers, cmd.x, cmd.y, apply_inpainting_mask)
            gimp_functions.open_images(cmd.images)
            cmd.img.undo_group_end()

        # TODO unpack, create layers, open images, etc.

    except Exception as e:
        print("Error: " + str(e))
        
