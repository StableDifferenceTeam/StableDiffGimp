import gimpfu
import stabledifference as sdiff
from Command import StableDiffusionCommand
from Command import StableBoyCommand


class Uncrop(StableDiffusionCommand):  # change to stablediffusioncommand
    #uri = "sdapi/v1/img2img"
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
            (gimpfu.PF_INT, "padding_left", "Padding Left", 100),
            (gimpfu.PF_INT, "padding_right", "Padding Right", 100),
            (gimpfu.PF_INT, "padding_top", "Padding Top", 100),
            (gimpfu.PF_INT, "padding_bottom", "Padding Bottom", 100),

        ],
        [],
    )

    # first, make the canvas the size of the image, plus padding
    
    #def __init__(self, **kwargs):
    #    StableBoyCommand.__init__(self, **kwargs)
        
        #StableDiffusionCommand.__init__(self, **kwargs)

    def _make_request_data(self, **kwargs):
        StableDiffusionCommand._resize_canvas(self, **kwargs)
        return StableDiffusionCommand._make_request_data(self, **kwargs)


    #def run(self, **kwargs):
    #    params = self.metadata.params
    #    print(params)
    #    #kwargs.update(
    #    #    dict(zip(["padding_left", "padding_right", "padding_top", "padding_bottom"], (param[3] for param in self.metadata.params[]))))
    #    kwargs.update(dict(zip(["padding_left", "padding_right", "padding_top", "padding_bottom"], [params[3][3], params[4][3], params[5][3], params[6][3]])))
    #    print(kwargs)
    #    print("-----------------------------------")
    #    print(self.metadata.params)
    #    StableDiffusionCommand._resize_canvas(self, **kwargs)
    #    StableBoyCommand.run(self)

 
        