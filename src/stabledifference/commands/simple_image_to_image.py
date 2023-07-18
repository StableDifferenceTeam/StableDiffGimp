# image-to-image command (simplified)
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
from image_to_image import ImageToImageCommand


class SimpleTextToImageCommand(ImageToImageCommand):
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleImageToImageCommand",
        "StableDifference " + sdiff.__version__ + ": Image to Image - Simple mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Image to Image/Simple mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            (gimpfu.PF_SLIDER, 'denoising_strength',
             'Denoising Strength %', 50, (0, 100, 1)),
        ],
        [],
    )
