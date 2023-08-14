import stabledifference as sdiff
from Command import StableDifferenceCommand
import json
import os
import platform
from urlparse import urlparse
from gimpfu import *


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
        ("STRING", "prompt_gen_api_base_url", "Prompt generators API base URL,\n<small>(leave empty for deactivating it)</small>", old_prompt_gen_url),
        ("OPTION", 'styling', 'Styling', sdiff.constants.STYLING_THEMES.index(old_styling), sdiff.constants.STYLING_THEMES),

    ]
    # prevent theme changing in Linux as it may cause GTK bugs to appear
    if platform.uname()[0] == 'Linux':
        simple_args = [
        ("STRING", "api_base_url", "Stable Diffusion API base URL", old_url),
        ("STRING", "prompt_gen_api_base_url", "Prompt generators API base URL,\nleave empty for deactivating it", old_prompt_gen_url),
    ]
        
    # check if the string that is supposed to be an url to an api could be one
    # display a message to the user if it may be invalid, but just return it anyway
    def __validate_url__(self, url):

        # the case of the url being empty
        if len(url) is 0:
            return url
        
        #add http prefix if necessary
        if not url[0:4] == 'http':
            url='http://'+url
        parsed_url=urlparse(url)

        #check if it fullfills url structure
        if not bool(parsed_url.scheme and parsed_url.netloc and not parsed_url.path):
            print("The URL might be invalid: "+url)
            pdb.gimp_message_set_handler(MESSAGE_BOX)
            pdb.gimp_message("An URL you entered seems to be invalid: Please check it in the settings!")
        return url
    

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)

        # check if a sd api url has been entered
        if(len(kwargs['api_base_url']) is 0):
            pdb.gimp_message_set_handler(MESSAGE_BOX)
            pdb.gimp_message("The Stable Diffusion api url is empty, please check it in the settings!")
        

        # save the sd api url/prompt gen api url/theme to the settings file (including the linux case)
        # also check whether the url is a valid one
        if platform.uname()[0] != 'Linux':
            if 'api_base_url' in kwargs and 'styling' in kwargs and 'prompt_gen_api_base_url' in kwargs:
                with open(os.path.join(self.path, "settings.json"), 'w') as f:
                   json.dump({
                       'api_base_url': self.__validate_url__(kwargs['api_base_url']),
                       'styling': sdiff.constants.STYLING_THEMES[kwargs['styling']],
                       'prompt_gen_api_base_url': self.__validate_url__(kwargs['prompt_gen_api_base_url'])
                              }, f)
        else:
            if 'api_base_url' in kwargs and 'prompt_gen_api_base_url' in kwargs:
                with open(os.path.join(self.path, "settings.json"), 'w') as f:
                   json.dump({
                       'api_base_url': self.__validate_url__(kwargs['api_base_url']),
                       'styling': 'None',
                       'prompt_gen_api_base_url': self.__validate_url__(kwargs['prompt_gen_api_base_url'])
                              }, f)
