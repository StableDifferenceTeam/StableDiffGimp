# image-to-image command
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class ImageToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "ImageToImageCommand",
        #"Stable Boy " + sdiff.__version__ + " - Text to Image",
        "StableDifference " + sdiff.__version__ + ": Image to Image - Expert mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Image to Image/Expert mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            (gimpfu.PF_SLIDER, 'denoising_strength',
             'Denoising Strength %', 50, (0, 100, 1)),
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

    def _make_request_data(self, **kwargs):
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        request_data['denoising_strength'] = float(
            kwargs.get('denoising_strength', 75)) / 100
        request_data['init_images'] = [sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)]
        return request_data
