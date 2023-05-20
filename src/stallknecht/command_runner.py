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

from gimpfu import *

# Basic Command runner, no progress updates


def run_command(cmd):
    cmd.start()
    cmd.join()
    # gimp.progress_update(1.0)


def run_stable_diffusion_command(cmd):
    try:
        cmd.start()
        # TODO add some progress updates here (aesthetics)

        while cmd.status != "DONE":
            pass  # gimp.progress_update(cmd.progress)
        cmd.join()

        # TODO unpack, create layers, open images, etc.

    except Exception as e:
        print("Error: " + str(e))
