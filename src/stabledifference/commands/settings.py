# Settings command
import gimpfu
import stabledifference as sdiff
#from gimpshelf import shelf
from Command import StableBoyCommand


class SettingsCommand(StableBoyCommand):
    uri = "sdapi/v1/settings"
    metadata = StableBoyCommand.CommandMetadata( # proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results
        "SettingsCommand", # proc_name
        "Not Stable Boy " + sdiff.__version__ + "- Settings", # blurb
        "StableDiffusion Plugin for GIMP", # help
        "StableDifference", # author
        "StableDifference", # copyright
        "2023", # date
        "<Image>/StableDifference/Settings", # label
        "*", # imagetypes
        [ #params
            #(gimpfu.PF_BOOL, 'expert_mode', "Expert Mode", shelf['expert_mode']),
            (gimpfu.PF_STRING, 'api_base_url', 'API Base URL', "API Base URL", "balabasldfburl")#shelf['api_base_url'])
            # add extra settings here; if you add settings, make sure to also add them in stable_difference.py for initialization
        ],
        [], # results
    )

    def __init__(self, **kwargs):
        StableBoyCommand.__init__(self, **kwargs)
        # save settings in db using shelf (shelf works using a key defined here to save information until gimp is shutdown.)
        #shelf['expert_mode'] = [kwargs['expert_mode']]
        #shelf['api_base_url'] = [kwargs['api_base_url']]
        print("fuck it we ball")