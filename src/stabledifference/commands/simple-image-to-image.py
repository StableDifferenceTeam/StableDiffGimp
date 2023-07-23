# image-to-image command (simplified)
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class SimpleImageToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleImageToImageCommand",
        "Stable Boy " + sdiff.__version__ + " - Text to Image",
        #"StableDifference " + sdiff.__version__ + ": Image to Image - Simple mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Image to Image/Simple mode",  # menu path
        "*", [
            #(gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            #(gimpfu.PF_SLIDER, 'denoising_strength',
            # 'Denoising Strength %', 50, (0, 100, 1)),
        ],
        [],
    )

    def _make_request_data(self, **kwargs):
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        request_data['denoising_strength'] = float(
            kwargs.get('denoising_strength', 50)) / 100
        request_data['init_images'] = [sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)]
        return request_data
