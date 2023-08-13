import stabledifference as sdiff
from Command import StableDifferenceCommand
import json
import os
import platform


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

    # get the path where the plugin is located. 
    # The chain of 'dirname' calls is necessary to get into the folder where the settings.json file usually sits
    # Other methods would make multi plattform compability way more complicated
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(os.path.dirname(os.path.dirname(path)))

    # Open settings.json
    with open(os.path.join(path, "settings.json"), 'r') as f:
       settings = json.load(f)

       # Load the settings
       old_url = settings['api_base_url']
       old_prompt_gen_url = settings['prompt_gen_api_base_url']
       old_styling = settings['styling']


    # arguments for the gtk dialog are the api urls here
    simple_args = [
        ("STRING", "api_base_url", "Stable Diffusion API base URL", old_url),
        ("STRING", "prompt_gen_api_base_url", "Prompt generators API base URL,\nleave empty for deactivating it", old_prompt_gen_url),
        ("OPTION", 'styling', 'Styling', sdiff.constants.STYLING_THEMES.index(old_styling), sdiff.constants.STYLING_THEMES),

    ]
    # prevent theme changing in Linux as it may cause GTK bugs to appear
    if platform.uname()[0] == 'Linux':
        simple_args = [
        ("STRING", "api_base_url", "Stable Diffusion API base URL", old_url),
        ("STRING", "prompt_gen_api_base_url", "Prompt generators API base URL,\nleave empty for deactivating it", old_prompt_gen_url),
    ]
    

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)
        

        # save the sd api url/prompt gen api url/theme to the settings file (including the linux case)
        if platform.uname()[0] != 'Linux':
            if 'api_base_url' in kwargs and 'styling' in kwargs and 'prompt_gen_api_base_url' in kwargs:
                with open(os.path.join(self.path, "settings.json"), 'w') as f:
                   json.dump({
                       'api_base_url': kwargs['api_base_url'],
                       'styling': sdiff.constants.STYLING_THEMES[kwargs['styling']],
                       'prompt_gen_api_base_url': kwargs['prompt_gen_api_base_url']
                              }, f)
        else:
            if 'api_base_url' in kwargs and 'prompt_gen_api_base_url' in kwargs:
                with open(os.path.join(self.path, "settings.json"), 'w') as f:
                   json.dump({
                       'api_base_url': kwargs['api_base_url'],
                       'styling': 'None',
                       'prompt_gen_api_base_url': kwargs['prompt_gen_api_base_url']
                              }, f)
