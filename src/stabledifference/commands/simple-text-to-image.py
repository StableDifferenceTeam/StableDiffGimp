# text-to-image command (simplified)
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class SimpleCommand(StableDiffusionCommand):
    uri = "sdapi/v1/text-to-image"
    metadata = StableDiffusionCommand.CommandMetadata(
        "TextToImageSimpleCommand",
        "StableDifference Text to Image (Simplified) Command " + "v1",  # sdiff.__version__,
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Text to Image/Simple mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "Enter your Prompt here", ""),
            (gimpfu.PF_STRING, "negative_prompt", "Negative Prompt", ""),           
        ],
        [],
    )