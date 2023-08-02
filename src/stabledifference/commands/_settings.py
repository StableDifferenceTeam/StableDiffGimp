import stabledifference as sdiff
from Command import StableDifferenceCommand
import json
import os


class SettingsCommand(StableDifferenceCommand):
    metadata = StableDifferenceCommand.CommandMetadata(
        "SettingsCommand",  # proc_name
        "StableDifference " + sdiff.__version__ + ": Settings", # blurb
        "StableDiffusion Plugin for GIMP",  # help
        "StableDifference",  # author
        "StableDifference",  # copyright
        "2023",  # date
        "<Image>/StableDifference/ Settings",  # label
        "*",  # imagetypes
        [], # params
        [],  # results
    )
    name = "Settings"

    # use the api url from the settings file as default
    old_url = sdiff.constants.DEFAULT_API_URL
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    with open(os.path.join(path, "settings.json"), 'r') as f:
       settings = json.load(f)
       old_url = settings['api_base_url']

    # arguments for the gtk dialog is only the api url here
    simple_args = [
        ("STRING", "api_base_url", "API base URL", old_url),
    ]
    

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)

        # save the api url to the settings file
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
        with open(os.path.join(path, "settings.json"), 'w') as f:
           json.dump({'api_base_url': kwargs.get('api_base_url', sdiff.constants.DEFAULT_API_URL)}, f)
