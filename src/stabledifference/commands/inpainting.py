import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
from image_to_image import ImageToImageCommand

# InpaintingCommand class, inherits from ImageToImageCommand
class InpaintingCommand(ImageToImageCommand):
    # set the same API endpoint as ImageToImageCommand
    uri = "sdapi/v1/img2img"
    # define metadata for the command, including name, version, authors, date, and available parameters
    metadata = StableDiffusionCommand.CommandMetadata(
        "InpaintingImageCommand",
        "StableDifference " + sdiff.__version__ + ": Inpainting",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Inpainting",  # menu path
        "*",
        [],
        [],
    )
    # command name displayed to the user
    name = "Inpainting"
    # simple arguments that the user sees by default in the dialog box
    simple_args = [
        ("STRING", "prompt", "Prompt", ""),
        ("SLIDER", "denoising_strength",
         "Denoising strength %", 75.0, (0, 100, 1, 0)),
        ("SLIDER", "steps", "Steps", 25, (1, 150, 25, 1)),
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
        ("OPTION", 'inpainting_fill', 'Inpainting fill',
         1, sdiff.constants.INPAINTING_FILL_MODE),
        ("BOOL", 'inpaint_full_res', 'Inpaint at full resolution', 'True'),
        ("SLIDER", 'inpaint_full_res_padding',
            'Full res. inpainting padding', 0, (0, 128, 1, 0)),
        ("BOOL", 'autofit_inpainting', 'Autofit inpainting region', 'True'),
        ("SLIDER", 'mask_blur', 'Mask blur', 4, (0, 32, 1, 0)),
        ("BOOL", 'apply_inpainting_mask', 'Apply inpainting mask', 'True'),
    ]

    # constructor, initializes specific properties for inpainting
    def __init__(self, **kwargs):
        # set command specific parameters
        self.autofit_inpainting = kwargs.get('autofit_inpainting', True)
        self.apply_inpainting_mask = True
        self.apply_inpainting_mask = kwargs.get('apply_inpainting_mask', True)
        # call parent constructor
        ImageToImageCommand.__init__(self, **kwargs)

    # method to construct request data for inpainting, extends the parent class's method
    def _make_request_data(self, **kwargs):
        # call parent's method to construct basic request data
        req_data = ImageToImageCommand._make_request_data(self, **kwargs)
        # add inpainting specific parameters to request data
        req_data['inpainting_mask_invert'] = 1
        req_data['inpainting_fill'] = int(kwargs.get('inpainting_fill', 1))
        req_data['mask_blur'] = kwargs.get('mask_blur', 4)
        req_data['inpaint_full_res'] = kwargs.get('inpaint_full_res', True)
        req_data['inpaint_full_res_padding'] = kwargs.get(
            'inpaint_full_res_padding', 0)
        req_data['mask'] = sdiff.gimp.encode_mask(
            self.img, self.x, self.y, self.width, self.height)
        return req_data

    # method to determine the active inpainting area
    def _determine_active_area(self):

        if self.autofit_inpainting:
            # auto-fit the inpainting area if the option is enabled
            return sdiff.gimp.autofit_inpainting_area(self.img)
        else:
            # call parent's method to determine the active area
            return StableDiffusionCommand._determine_active_area(self)
