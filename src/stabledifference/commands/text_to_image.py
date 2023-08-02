import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand

# class inherits from StableDiffusionCommand and defines a command
# to transform text into an image using StableDifference. 
class TextToImageCommand(StableDiffusionCommand):
    # URI endpoint for the text to image conversion
    uri = "sdapi/v1/txt2img"
    # command metadata for registering the command with GIMP.
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleTextToImageCommand",
        "StableDifference " + sdiff.__version__ + ": Text to Image",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Text to Image",  # menu path
        "*",
        [],
        [],
    )
    # command name displayed to the user
    name = "Text to Image"
    # simple arguments that the user sees by default in the dialog box
    simple_args = [
        ("STRING", "prompt", "Prompt", ""),
        ("SLIDER", 'steps', 'Steps', 25, (1, 150, 1, 0)),
    ]
    # expert arguments that the user can access through advanced settings
    expert_args = [
        ("STRING", "negative_prompt", "Negative Prompt", ""),
        ("STRING", 'seed', 'Seed', '-1'),
        ("OPTION", 'sampler_index', 'Sampler', 0, sdiff.constants.SAMPLERS),
        ("BOOL", 'restore_faces', 'Restore faces', 'False'),
        ("SLIDER", 'cfg_scale', 'CFG', 7.5, (0, 20, 0.5, 1)),
        ("SPIN_BTN", 'num_images', 'Number of images', 1, (1, 4, 1)),
        ("OPTION", 'img_target', 'Results as', 0, sdiff.constants.IMAGE_TARGETS),
    ]
