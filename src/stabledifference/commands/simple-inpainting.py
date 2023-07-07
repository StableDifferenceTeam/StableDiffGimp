# Inpainting command
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class ImageToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "ImageToImageCommand",
        #"Stable Boy " + sdiff.__version__ + " - Text to Image",
        "StableDifference " + sdiff.__version__ + ": Inpainting - Simple mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Inpainting",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            

        ],
        [],
    )

    def _make_request_data(self, **kwargs):
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        request_data['denoising_strength'] = float(
            kwargs['denoising_strength']) / 100
        request_data['init_images'] = [sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)]
        return request_data