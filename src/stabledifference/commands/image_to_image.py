import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand


class ImageToImageCommand(StableDiffusionCommand):
    uri = "sdapi/v1/img2img"  # uri for image-to-image command
    metadata = StableDiffusionCommand.CommandMetadata(
        "ImageToImageCommand",
        "StableDifference " + sdiff.__version__ + ": Image to Image",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Image to Image",  # menu path
        "*",
        [],
        [],
    )

    name = "Image to Image"

    # the arguments needed when using 'simple mode'/the options aren't expanded + their default values
    simple_args = [
        ("STRING", "prompt", "Prompt", ""),
        ("SLIDER", 'denoising_strength',
         'Denoising Strength %', 50, (0, 100, 1, 0))
    ]

    # if the window has been expanded/'expert mode' is being used
    expert_args = [
        ("STRING", "negative_prompt", "Negative Prompt", ""),
        ("STRING", 'seed', 'Seed', '-1'),
        ("SLIDER", 'steps', 'Steps', 25, (1, 150, 1, 0)),
        ("OPTION", 'sampler_index', 'Sampler', 0, sdiff.constants.SAMPLERS),
        ("BOOL", 'restore_faces', 'Restore faces', 'False'),
        ("SLIDER", 'cfg_scale', 'CFG', 7.5, (0, 20, 0.5, 1)),
        ("SPIN_BTN", 'num_images', 'Number of images', 1, (1, 4, 1)),
        ("OPTION", 'img_target', 'Results as', 0, sdiff.constants.IMAGE_TARGETS),
    ]

    def _make_request_data(self, **kwargs):
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        # convert denoising strength to float between 0 and 1
        request_data['denoising_strength'] = float(
            kwargs.get('denoising_strength', 75)) / 100
        # use the image as the initial image
        request_data['init_images'] = [sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)]
        return request_data
