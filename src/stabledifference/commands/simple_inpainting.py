# Inpainting command
import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
from inpainting import InpaintingCommand


class SimpleInpaintingCommand(InpaintingCommand):
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleInpaintingImageCommand",
        "StableDifference " + sdiff.__version__ + ": Inpainting - Simple mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Inpainting/Simple mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, 'prompt', 'Prompt', ''),
            (gimpfu.PF_SLIDER, 'steps', 'Steps', 25, (1, 150, 25)),
            #(gimpfu.PF_OPTION, 'sampler_index', 'Sampler', 0, sdiff.constants.SAMPLERS),
            #(gimpfu.PF_SLIDER, 'cfg_scale', 'CFG', 7.5, (0, 20, 0.5)),
            #(gimpfu.PF_SLIDER, 'denoising_strength', 'Denoising strength %', 75.0, (0, 100, 1)),
            #(gimpfu.PF_BOOL, 'autofit_inpainting', 'Autofit inpainting region', True),
            #(gimpfu.PF_SLIDER, 'mask_blur', 'Mask blur', 4, (0, 32, 1)),
            #(gimpfu.PF_OPTION, 'inpainting_fill', 'Inpainting fill', 3, sdiff.constants.INPAINTING_FILL_MODE),
            #(gimpfu.PF_BOOL, 'inpaint_full_res', 'Inpaint at full resolution', True),
            #(gimpfu.PF_INT, 'inpaint_full_res_padding', 'Full res. inpainting padding', 0),
            #(gimpfu.PF_OPTION, 'img_target', 'Results as', 0, sdiff.constants.IMAGE_TARGETS),
            #(gimpfu.PF_BOOL, 'apply_inpainting_mask', 'Apply inpainting mask', True),
        ],
        [],
    )
    
    #def __init__(self, **kwargs):
    #    self.autofit_inpainting = kwargs.get('autofit_inpainting', True)
    #    self.apply_inpainting_mask = True
    #    self.apply_inpainting_mask = kwargs.get('apply_inpainting_mask', True)
    #    ImageToImageCommand.__init__(self, **kwargs)
#
    #def _make_request_data(self, **kwargs):
    #    req_data = ImageToImageCommand._make_request_data(self, **kwargs)
    #    req_data['inpainting_mask_invert'] = 1
    #    req_data['inpainting_fill'] = kwargs.get('inpainting_fill', 3)
    #    req_data['mask_blur'] = kwargs.get('mask_blur', 4)
    #    req_data['inpaint_full_res'] = kwargs.get('inpaint_full_res', True)
    #    req_data['inpaint_full_res_padding'] = kwargs.get('inpaint_full_res_padding', 0)
    #    req_data['mask'] = sdiff.gimp.encode_mask(self.img, self.x, self.y, self.width, self.height)
    #    return req_data
#
    #def _determine_active_area(self):
    #    if self.autofit_inpainting:
    #        return sdiff.gimp.autofit_inpainting_area(self.img)
    #    else:
    #        return StableDiffusionCommand._determine_active_area(self)