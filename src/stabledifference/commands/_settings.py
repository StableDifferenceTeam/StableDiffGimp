# Settings command
import gimpfu
import stabledifference as sdiff
#from gimpshelf import shelf
from Command import StableDifferenceCommand
import json
import os


class SettingsCommand(StableDifferenceCommand):
    uri = "sdapi/v1/settings"
    metadata = StableDifferenceCommand.CommandMetadata(  # proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results
        "SettingsCommand",  # proc_name
        "Not Stable Boy " + sdiff.__version__ + "- Settings",  # blurb
        "StableDiffusion Plugin for GIMP",  # help
        "StableDifference",  # author
        "StableDifference",  # copyright
        "2023",  # date
        "<Image>/StableDifference/Settings",  # label
        "*",  # imagetypes
        [  # params
            #(gimpfu.PF_BOOL, 'expert_mode', "Expert Mode", shelf['expert_mode']),
            # (gimpfu.PF_STRING, 'api_base_url', 'API Base URL',
            # "API Base URL", "balabasldfburl")  # shelf['api_base_url'])
            # add extra settings here; if you add settings, make sure to also add them in stable_difference.py for initialization
        ],
        [],  # results
    )
    name = "Settings"
    old_url = sdiff.constants.DEFAULT_API_URL

    # if not os.path.isfile('settings.json'):
    #    print("settings.json does not exist")
    #    #os.makedirs(os.path.dirname('settings.json'), exist_ok=True)
    #    with open('settings.json', 'x') as f:
    #        pass
    #    f.write('{"api_base_url": "' + old_url + '"}')
    # with open('settings.json', 'r') as f:
    #    settings = json.load(f)
    #    old_url = settings['api_base_url']

    simple_args = [
        ("STRING", "api_base_url", "API base URL", old_url),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # save settings in db using shelf (shelf works using a key defined here to save information until gimp is shutdown.)
        #shelf['expert_mode'] = [kwargs['expert_mode']]
        #shelf['api_base_url'] = [kwargs['api_base_url']]
        print("fuck it we ball")
        # open file settings.json and save 'api_base_url' as the new kwargs['api_base_url']

        # with open('settings.json', 'r') as f:
        #    settings = json.load(f)
        #    settings['api_base_url'] = kwargs['api_base_url']
        # with open('settings.json', 'w') as f:
        #    json.dump(settings, f)
