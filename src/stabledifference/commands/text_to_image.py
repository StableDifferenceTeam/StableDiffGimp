import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class TextToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/txt2img"
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
    name = "Text to Image"
    
    # the arguments needed when using 'simple mode'/the options aren't expanded + their default values
    simple_args = [
        ("STRING", "prompt", "Prompt", ""),
        ("SLIDER", 'steps', 'Steps', 25, (1, 150, 1, 0)),
    ]

    # if the window has been expanded/'expert mode' is being used
    expert_args = [
        ("STRING", "negative_prompt", "Negative Prompt", ""),
        ("STRING", 'seed', 'Seed', '-1'),
        ("OPTION", 'sampler_index', 'Sampler', 0, sdiff.constants.SAMPLERS),
        ("BOOL", 'restore_faces', 'Restore faces', 'False'),
        ("SLIDER", 'cfg_scale', 'CFG', 7.5, (0, 20, 0.5, 1)),
        ("SPIN_BTN", 'num_images', 'Number of images', 1, (1, 4, 1)),
        ("OPTION", 'img_target', 'Results as', 0, sdiff.constants.IMAGE_TARGETS),
    ]
