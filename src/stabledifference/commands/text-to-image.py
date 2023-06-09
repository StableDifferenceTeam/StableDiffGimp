# text-to-image command
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class TextToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/txt2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "TextToImageCommand",
        "Stable Boy " + sdiff.__version__ + " - Text to Image",#"StableDifference Text to Image Command " + "v1",  # sdiff.__version__,
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Text to Image/Expert mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "Enter your Prompt here", ""),
            (gimpfu.PF_STRING, "negative_prompt", "Negative Prompt", ""),
            (gimpfu.PF_STRING, 'seed', 'Seed', '-1'),
            (gimpfu.PF_SLIDER, 'steps', 'Steps', 25, (1, 150, 25)),
            (gimpfu.PF_OPTION, 'sampler_index',
             'Sampler', 0, sdiff.constants.SAMPLERS),
            (gimpfu.PF_BOOL, 'restore_faces', 'Restore faces', False),
            (gimpfu.PF_SLIDER, 'cfg_scale', 'CFG', 7.5, (0, 20, 0.5)),
            (gimpfu.PF_SLIDER, 'num_images', 'Number of images', 1, (1, 4, 1)),
            (gimpfu.PF_OPTION, 'img_target', 'Results as',
             0, sdiff.constants.IMAGE_TARGETS),
            
        ],
        [],
    )
