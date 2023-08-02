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
    old_prompt_gen_url = sdiff.constants.DEFAULT_PROMPT_GEN_API_URL
    old_styling = sdiff.constants.STYLING_THEMES[1]

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    with open(os.path.join(path, "settings.json"), 'r') as f:
       settings = json.load(f)
       old_url = settings['api_base_url']
       old_prompt_gen_url = settings['prompt_gen_api_base_url']
       old_styling = settings['styling']

    # arguments for the gtk dialog are the api urls here
    simple_args = [
        ("STRING", "api_base_url", "Stable Diffusion API base URL", old_url),
        ("STRING", "prompt_gen_api_base_url", "Prompt generators API base URL,\nleave empty for deactivating it", old_prompt_gen_url),
        ("OPTION", 'styling', 'Styling', sdiff.constants.STYLING_THEMES.index(old_styling), sdiff.constants.STYLING_THEMES),

    ]
    

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)

        # save the api url to the settings file
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
        if 'api_base_url' in kwargs and 'styling' in kwargs and 'prompt_gen_api_base_url' in kwargs:
            with open(os.path.join(path, "settings.json"), 'w') as f:
               json.dump({
                   'api_base_url': kwargs['api_base_url'],
                   'styling': sdiff.constants.STYLING_THEMES[kwargs['styling']],
                   'prompt_gen_api_base_url': kwargs['prompt_gen_api_base_url']
                          }, f)
