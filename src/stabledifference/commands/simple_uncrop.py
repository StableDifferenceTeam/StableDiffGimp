import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
from Command import StableBoyCommand
from image_to_image import ImageToImageCommand
import hashlib


class Uncrop(ImageToImageCommand):  # change to stablediffusioncommand
    uri = "sdapi/v1/img2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleUncropToImageCommand",
        "StableDifference " + sdiff.__version__ + ": Uncrop - Simple mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Uncrop/Simple mode",  # menu path
        "*", [
            (gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            (gimpfu.PF_SLIDER, "padding_left", "Padding left", 128, (0, 256, 1)),
            (gimpfu.PF_SLIDER, "padding_right", "Padding right", 128, (0, 256, 1)),
            (gimpfu.PF_SLIDER, "padding_top", "Padding top", 128, (0, 256, 1)),
            (gimpfu.PF_SLIDER, "padding_bottom",
             "Padding bottom", 128, (0, 256, 1)),
        ],
        [],
    )

    def __init__(self, **kwargs):
        ImageToImageCommand.__init__(self, **kwargs)
        self.padding_left = kwargs.get('padding_left', 128)
        self.padding_right = kwargs.get('padding_right', 128)
        self.padding_top = kwargs.get('padding_top', 128)
        self.padding_bottom = kwargs.get('padding_bottom', 128)

    def _make_request_data(self, **kwargs):
        request_data = ImageToImageCommand._make_request_data(self, **kwargs)
        StableDiffusionCommand._resize_canvas(self, **kwargs)

        request_data['script_name'] = "Outpainting mk2"

        # ----------------- script args -----------------
        script_args = [0]
        # padding
        pad_left, pad_right, pad_top, pad_btm = kwargs.get(
            'padding_left', 128), kwargs.get('padding_right', 128), kwargs.get('padding_top', 128), kwargs.get('padding_bottom', 128)
        max_padding = max(pad_left, pad_right, pad_top, pad_btm)

        if max_padding > 128:
            script_args.append(256)
        elif max_padding == 0:
            raise Exception("Padding must be at least 1px")
        else:
            script_args.append(128)

        # mask blur
        script_args.append(kwargs.get('mask_blur', 8))
        # directions
        script_args.append([])
        if pad_left > 0:
            script_args[-1].append('left')
        if pad_right > 0:
            script_args[-1].append('right')
        if pad_top > 0:
            script_args[-1].append('up')
        if pad_btm > 0:
            script_args[-1].append('down')

        # fall-off exponent (lower=higher detail)
        script_args.append(kwargs.get('fall_off_exponent', 1.0))

        # color variation
        script_args.append(kwargs.get('color_variation', 0.05))

        request_data['script_args'] = script_args

        return request_data

    # def _process_response(self, resp):
#
    #    def _mk_short_hash(img):  # create hash for image
    #        return hashlib.sha1(img.encode("UTF-8")).hexdigest()[:7]
#
    #    all_imgs = resp['images']  # get images from response
#
    #    if self.img_target == 'Layers':  # if layers are the target
    #        self.layers = [StableDiffusionCommand.LayerResult(
    #            _mk_short_hash(img), img, None) for img in all_imgs]  # create layer result
    #        # translate layers
    #        for layer in self.layers:
    #            raise Exception(str(self.padding_left))
    #    elif self.img_target == 'Images':  # if images are the target
    #        self.images = all_imgs  # create image result

        # crop images to original size
        # for layer in self.layers:
        #    layer.gimp_image_crop(512, 512, 0, 0)
