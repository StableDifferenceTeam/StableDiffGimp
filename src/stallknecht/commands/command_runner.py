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
