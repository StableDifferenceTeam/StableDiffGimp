import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand

# ImageToImageCommand class, inherits from StableDiffusionCommand
class ImageToImageCommand(StableDiffusionCommand):

    # set the API endpoint for the image-to-image transformation
    uri = "sdapi/v1/img2img"  

    # define metadata for the command, including name, version, authors, date, and available parameters
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
    # command name displayed to the user
    name = "Image to Image"
    simple_args = [
        ("STRING", "prompt", "Prompt", ""),
        ("SLIDER", 'denoising_strength',
         'Denoising Strength %', 50, (0, 100, 1, 0))
    ]
    # expert arguments that the user can access through advanced settings
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

    # method to construct request data
    def _make_request_data(self, **kwargs):
        # call the parent class method to construct request data
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        # convert denoising strength to float between 0 and 1
        request_data['denoising_strength'] = float(
            kwargs.get('denoising_strength', 75)) / 100
        # add the encoded initial images to the request data
        request_data['init_images'] = [sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)]
        return request_data
