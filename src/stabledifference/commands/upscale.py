import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
import hashlib


class UpscaleCommand(StableDiffusionCommand):
    uri = "sdapi/v1/extra-single-image"
    metadata = StableDiffusionCommand.CommandMetadata(
        "UpscaleCommand",
        "StableDifference " + sdiff.__version__ + ": Upscale",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Upscale",  # menu path
        "*",
        [],
        [],
    )
    name = "Upscale"
    simple_args = [
        ("SLIDER", "upscaling_resize", "Upscaling Factor", 2, (2, 4, 1, 0)),
    ]
    expert_args = [
        ("OPTION", 'upscaler_1', 'Upscaler 1', 1, sdiff.constants.UPSCALERS),
        ("OPTION", 'upscaler_2', 'Upscaler 2', 0, sdiff.constants.UPSCALERS),
        ("SLIDER", "extras_upscaler_2_visibility",
         "Upscaler 2 Visibility", 0, (0, 1, 0.1, 1)),
    ]

    def __init__(self, **kwargs):
        StableDiffusionCommand.__init__(self, **kwargs)
        width = self.width
        height = self.height
        # calculate the padding on all sides equally
        upscaling_resize = int(kwargs.get('upscaling_resize', 2))
        self.padding_left = (width * upscaling_resize - width) / 2
        self.padding_right = (width * upscaling_resize - width) / 2
        self.padding_top = (height * upscaling_resize - height) / 2
        self.padding_bottom = (height * upscaling_resize - height) / 2

    def _make_request_data(self, **kwargs):
        request_data = {}
        # instead of 'images' we use 'image' for single image commands
        # we do it in the beginning, so the image is without recrop
        request_data['image'] = sdiff.gimp.encode_img(
            self.img, self.x, self.y, self.width, self.height)

        # padding on all sides is the image size times the upscaling factor - width / 2 - size
        width = self.width
        height = self.height
        upscaling_resize = int(kwargs.get('upscaling_resize', 2))
        kwargs.update({
            'padding_left': (width * upscaling_resize - width) / 2,
            'padding_right': (width * upscaling_resize - width) / 2,
            'padding_top': (height * upscaling_resize - height) / 2,
            'padding_bottom': (height * upscaling_resize - height) / 2,
        })
        # resize the canvas to the new size
        StableDiffusionCommand._resize_canvas(self, **kwargs)

        # set the request data
        request_data['upscaling_resize'] = int(
            kwargs.get('upscaling_resize', 2))
        request_data['upscaler_1'] = sdiff.constants.UPSCALERS[int(
            kwargs.get('upscaler_1', 1))]
        request_data['upscaler_2'] = sdiff.constants.UPSCALERS[int(
            kwargs.get('upscaler_2', 0))]
        request_data['extras_upscaler_2_visibility'] = float(
            kwargs.get('extras_upscaler_2_visibility', 0))
        return request_data

    def _process_response(self, resp):
        # create layer result
        def _mk_short_hash(img):  # create hash for image
            return hashlib.sha1(img.encode("UTF-8")).hexdigest()[:7]
        img = resp['image']
        self.layers = StableDiffusionCommand.LayerResult(
            _mk_short_hash(img), img, None)
