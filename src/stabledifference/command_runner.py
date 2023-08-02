import gtk
from gimpfu import *
import gimp_functions
from .config import Config as config
from time import time, sleep
import random
import stabledifference as sdiff

# Basic Command runner, no progress updates


def run_command(cmd):
    cmd.start()
    cmd.join()


def run_stable_diffusion_command(cmd):
    try:
        # open a new dialog for the progress bar
        dialog = gtk.Dialog(" ")
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_size_request(500, 70)
        dialog.set_resizable(False)
        dialog.set_modal(True)
        dialog.present()

        # create the progress bar
        progressbar = gtk.ProgressBar()
        progressbar.set_fraction(0.0)
        progressbar.set_pulse_step(0.1)
        progressbar.set_text("Processing...")

        # add the progress bar to the dialog
        dialog.vbox.pack_start(progressbar, True, True, 10)
        progressbar.show()
        dialog.show()

        # start the command
        cmd.start()

        i = 0
        progress_texts = sdiff.constants.PROGRESS_TEXTS
        # update the progress bar until the command is done or an error occurs
        while cmd.status != "DONE" and cmd.status != "ERROR":
            i += 1
            # change the text every 3 seconds
            if i % 30 == 0:
                new_text = progress_texts[random.randint(
                    0, len(progress_texts) - 1)]
                progressbar.set_text(new_text)

            progressbar.pulse()
            # update the dialog
            while gtk.events_pending():
                gtk.main_iteration()
            sleep(0.1)

        # Error handling: if the command failed, show the error message
        if cmd.status == "ERROR":

            pdb.gimp_message_set_handler(MESSAGE_BOX)
            pdb.gimp_message("-----------------------------------------------------------------------------------\n" +
                             "An error occurred while calling the generative model:\n" +
                             "-----------------------------------------------------------------------------------\n"+str(cmd.error_msg))

        # if the command succeeded
        else:
            # create Layers or Images depending on the mode
            cmd.join()
            cmd.img.undo_group_start()
            apply_inpainting_mask = hasattr(
                cmd, 'apply_inpainting_mask') and cmd.apply_inpainting_mask
            layers_names = gimp_functions.create_layers(
                cmd.img, cmd.layers, cmd.x, cmd.y, apply_inpainting_mask)
            gimp_functions.open_images(cmd.images)

            # for uncrop, crop and resize the layers to the desired size
            if layers_names != None:
                if cmd.uncrop:
                    cmd._rescale_uncrop(layers_names)

            cmd.img.undo_group_end()

    except Exception as e:
        print("Error: " + str(e))
