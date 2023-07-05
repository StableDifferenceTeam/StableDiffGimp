# Settings command
import gimpfu
import stabledifference as sdiff
from gimpshelf import shelf
from Command import StableDiffusionCommand


class SettingsCommand(StableDiffusionCommand):
    uri = "sdapi/v1/inpainting"
    metadata = StableDiffusionCommand.CommandMetadata( # proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results
        "SettingsCommand", # proc_name
        "Not Stable Boy " + sdiff.__version__ + "- Settings", # blurb
        "StableDiffusion Plugin for GIMP", # help
        "StableDifference", # author
        "StableDifference", # copyright
        "2023", # date
        "<Image>/StableDifference/Settings", # label
        "*", # imagetypes
        [ #params
            (gimpfu.PF_BOOL, 'expert_mode', "Expert Mode", False),
            (gimpfu.PF_STRING, 'api_base_url', 'API Base URL', "API Base URL", sdiff.constants.DEFAULT_API_URL)
            # add extra settings here
        ],
        [], # results
    )

    def __init__(self, **kwargs):
        # save settings in db using shelf (shelf works using a key defined here to save information until gimp is shutdown. (Problems may arise if these are not initiated TODO))
        shelf['expert_mode'] = [kwargs['expert_mode']]
        shelf['api_base_url'] = [kwargs['api_base_url']]