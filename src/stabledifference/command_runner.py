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
from time import time, sleep
import random

# Basic Command runner, no progress updates


def run_command(cmd):
    cmd.start()
    cmd.join()
    # gimp.progress_update(1.0)


def run_stable_diffusion_command(cmd):
    try:
        # open a new message dialog to show the progress bar
        dialog = gtk.Dialog(" ")
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_size_request(500, 50)
        dialog.set_resizable(False)
        dialog.set_modal(True)
        dialog.present()

        # create a progress bar
        progressbar = gtk.ProgressBar()
        progressbar.set_fraction(0.0)
        progressbar.set_pulse_step(0.1)
        progressbar.set_text("Processing...")

        # add the progress bar to the dialog
        dialog.vbox.pack_start(progressbar, True, True, 0)
        progressbar.show()
        dialog.show()

        cmd.start()

        i = 0
        progress_texts = [
            "AI is drawing...",
            "Unpacking Creativity...",
            "Igniting the AI's passion for painting...",
            "Stabilizing the diffusion...",
            "Constructing the masterpiece one pixel at a time...",
            "Generating the next Van Gogh...",
            "AI is taking a coffee break...",
            "Inspiriation is flowing...",
            "AI is thinking...",
            "Adding perspective...",
            "AI is painting...",
            "Putting life into the painting...",
            "Adding a sprinkle of magic to the artwork...",
            "Adding a touch of color...",
            "Adding the Background...",
            "AI is dancing with the muse of creativity...",
            "Cleaning digital brushes...",
            "AI is getting into the flow...",
            "Adding Love...",
            "AI is doing it's best (aren't we all?)..."
        ]
        while cmd.status != "DONE" and cmd.status != "ERROR":
            i += 1
            if i % 30 == 0:
                new_text = progress_texts[random.randint(
                    0, len(progress_texts) - 1)]
                progressbar.set_text(new_text)

            # update the progress bar
            progressbar.pulse()
            # update the dialog
            while gtk.events_pending():
                gtk.main_iteration()
            sleep(0.1)
        if cmd.status == "ERROR":
                                      
                          
            pdb.gimp_message_set_handler(MESSAGE_BOX)
            pdb.gimp_message("-----------------------------------------------------------------------------------\n"+
                             "An error occurred while calling the generative model:\n"+
                             "-----------------------------------------------------------------------------------\n"+str(cmd.error_msg))
        else:
            cmd.join()
            cmd.img.undo_group_start()
            apply_inpainting_mask = hasattr(
                cmd, 'apply_inpainting_mask') and cmd.apply_inpainting_mask
            layers_names = gimp_functions.create_layers(
                cmd.img, cmd.layers, cmd.x, cmd.y, apply_inpainting_mask)
            gimp_functions.open_images(cmd.images)
    
            if layers_names != None:
                if cmd.uncrop:
                    cmd._rescale_uncrop(layers_names)
    
            cmd.img.undo_group_end()

    except Exception as e:
        print("Error: " + str(e))
