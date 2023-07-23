
# Basic Command class, executable by the command runner
# class Command:
#    def __init__(self, **kwargs):
#        self.command_metadata = kwargs
#        self.status = "INITIALIZED"
#
#    def run(self):
#        self.status = "RUNNING"
#        print("Command is running")
#
#
# class StableDiffusionCommand(Command):
#
#    uri = ""
#
#    def __init__(self, command_metadata):
#        super().__init__(self, command_metadata)
#        self.url = urljoin("http://localhost:7860", self.uri)
#        self.img = command_metadata["img"]
#
#    def run(self):
#        self.status = "RUNNING"
#        print("Command is running")
#        self.progress = 0.5
#        self.status = "DONE"


import json
import socket
import hashlib
import tempfile
from threading import Thread
from urlparse import urljoin
from urllib2 import Request, urlopen
from collections import namedtuple
from stabledifference.command_runner import config
import stabledifference as sdiff
from stabledifference.constants import PREFERENCES_SHELF_GROUP as PREFS
import gimpfu
import gtk


class StableBoyCommand(Thread):
    LayerResult = namedtuple('LayerResult', 'name img children')
    # CommandMetadata is just the names of the parameters of the command
    CommandMetadata = namedtuple(
        'CommandMetadata', 'proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results')
    # we initialize the metadata with None, because it is set in the run_command method
    metadata = None
    command_runner = None

    @classmethod
    def run_command(cls, *args, **kwargs):
        # args is the actual parameters of the command, kwargs is where the parameters are stored in named variables
        # type: ignore
        kwargs.update(
            dict(zip((param[1] for param in cls.metadata.params), args)))
        sdiff.gimp.save_prefs(cls.metadata.proc_name, **kwargs)  # type: ignore
        # type: ignore <== command_runner runs an instance of command class
        cls.command_runner(cls(**kwargs))

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.status = 'INITIALIZED'

    # -----------------------------------------------------------------------

    @classmethod
    def _show_advanced_options(self, image, drawable, **kwargs):
        request_data = {}

        # Create a new GTK dialog
        dialog = gtk.Dialog(title='blabla - Expert mode')
        dialog.set_border_width(10)

        # Create a new GTK entry field for the prompt
        prompt_label = gtk.Label('Prompt')
        prompt_entry = gtk.Entry()
        prompt_entry.set_text('')

        # Create a new GTK button to show/hide the advanced options
        advanced_button = gtk.Button(label='Expand')
        advanced_button.connect(
            'clicked', lambda button: self._toggle_advanced_options(self, dialog, advanced_button))

        # Pack the prompt entry and the advanced button into the dialog
        dialog.vbox.pack_start(prompt_label, True, True, 0)
        dialog.vbox.pack_start(prompt_entry, True, True, 0)
        dialog.vbox.pack_start(advanced_button, True, True, 0)

        # Add the OK and Cancel buttons to the dialog
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        # Show the dialog
        dialog.show_all()

        # Run the dialog and get the response
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            kwargs.update({
                "image" : image,
                "drawable" : drawable, 
                "prompt" : prompt_entry.get_text()})
        ##request_data['sampler_index'] = sampler_index.get_active()
        #request_data['restore_faces'] = restore_faces.get_active()
        #request_data['cfg_scale'] = cfg_scale.get_value()
        #request_data['num_images'] = num_images.get_value()
        ##request_data['img_target'] = img_target.get_active()
        #request_data['negative_prompt'] = negative_prompt.get_text()
        #request_data['seed'] = seed.get_text()
        ##request_data['text'] = text


        dialog.destroy()

        # call the run_command function
        self.command_runner(self(**kwargs))
        #self.run_command(self, image, drawable, request_data)

        return request_data

    def _toggle_advanced_options(self, dialog, button):
        # Toggle the visibility of the advanced options
        if button.get_label() == 'Expand':
            button.set_label('Collapse')
            self._add_advanced_options(dialog)
        else:
            button.set_label('Expand')
            self._remove_advanced_options(dialog)

    def _add_advanced_options(dialog):
        # Create the advanced options widgets
        restore_faces = gtk.CheckButton(label='Restore faces')

        cfg_scale_label = gtk.Label('CFG')
        cfg_scale = gtk.HScale()
        cfg_scale.set_range(0, 20)
        cfg_scale.set_increments(0.5, 1)
        cfg_scale.set_value(7.5)

        num_images_label = gtk.Label('Number of images')
        num_images = gtk.SpinButton()
        num_images.set_range(1, 4)
        num_images.set_increments(1, 1)
        num_images.set_value(1)

        negative_prompt_label = gtk.Label('Negative Prompt')
        negative_prompt = gtk.Entry()

        seed_label = gtk.Label('Seed')
        seed = gtk.Entry()
        seed.set_text('-1')

        # Pack the advanced options into the dialog
        dialog.vbox.pack_start(restore_faces, True, True, 0)
        dialog.vbox.pack_start(cfg_scale_label, True, True, 0)
        dialog.vbox.pack_start(cfg_scale, True, True, 0)
        dialog.vbox.pack_start(num_images_label, True, True, 0)
        dialog.vbox.pack_start(num_images, True, True, 0)
        dialog.vbox.pack_start(negative_prompt_label, True, True, 0)
        dialog.vbox.pack_start(negative_prompt, True, True, 0)
        dialog.vbox.pack_start(seed_label, True, True, 0)
        dialog.vbox.pack_start(seed, True, True, 0)

        # Show the advanced options
        dialog.show_all()

    def _remove_advanced_options(dialog):
        # Remove the advanced options from the dialog
        for child in dialog.vbox.get_children():
            if child != dialog.action_area.get_children()[0]:
                dialog.vbox.remove(child)
        dialog.show_all()
    # -----------------------------------------------------------------------


class StableDiffusionCommand(StableBoyCommand):
    uri = ''

    def __init__(self, **kwargs):
        StableBoyCommand.__init__(self, **kwargs)
        self.url = urljoin(sdiff.gimp.pref_value(
            PREFS, 'api_base_url', sdiff.constants.DEFAULT_API_URL), self.uri)  # api URL TODO shelf url aus settings?
        self.img = kwargs['image']  # image to be processed
        self.images = None  # images to be processed
        self.layers = None  # layers to be processed

        self.x, self.y, self.width, self.height = self._determine_active_area()  # active area

        print('x, y, w, h: ' + str(self.x) + ', ' + str(self.y) +
              ', ' + str(self.width) + ', ' + str(self.height))

        self.img_target = sdiff.constants.IMAGE_TARGETS[kwargs.get(
           'img_target', 0)]  # layers are the default img_target

        self.req_data = self._make_request_data(**kwargs)
        if config.TIMEOUT_REQUESTS:
           self.timeout = self._estimate_timeout(self.req_data)
        else:
           self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT  # type: ignore

    def run(self):
        self.status = 'RUNNING'
        try:
            # prints out a request path
            if config.LOG_REQUESTS:
                req_path = tempfile.mktemp(prefix='req_', suffix='.json')
                with open(req_path, 'w') as req_file:
                    print('request: ' + req_path)
                    req_file.write(json.dumps(self.req_data))

            sd_request = Request(url=self.url,
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.req_data))  # request data
            # print(self.req_data)
            self.sd_resp = urlopen(
                sd_request, timeout=self.timeout)  # start request
            if self.sd_resp:
                self.response = json.loads(
                    self.sd_resp.read())  # read response
                if config.LOG_REQUESTS:
                    # create temporary response file
                    resp_path = tempfile.mktemp(prefix='resp_', suffix='.json')
                    with open(resp_path, 'w') as resp_file:  # write response to file
                        print('response: ' + resp_path)
                        resp_file.write(json.dumps(self.response))

                # process response (see below)
                self._process_response(self.response)

            self.status = 'DONE'

        except Exception as e:  # catch ERROR
            self.status = 'ERROR'
            self.error_msg = str(e)
            print(e)
            raise e

    def _process_response(self, resp):

        def _mk_short_hash(img):  # create hash for image
            return hashlib.sha1(img.encode("UTF-8")).hexdigest()[:7]

        all_imgs = resp['images']  # get images from response
        if self.img_target == 'Layers':  # if layers are the target
            self.layers = [StableDiffusionCommand.LayerResult(
                _mk_short_hash(img), img, None) for img in all_imgs]  # create layer result
        elif self.img_target == 'Images':  # if images are the target
            self.images = all_imgs  # create image result

    def _determine_active_area(self):
        return sdiff.gimp.active_area(self.img)

    def _make_request_data(self, **kwargs):
        return {
            'prompt': kwargs.get('prompt', ''),
            'negative_prompt': kwargs.get('negative_prompt', ''),
            'steps': kwargs.get('steps', 25),
            'sampler_index': sdiff.constants.SAMPLERS[kwargs.get('sampler_index', 0)],
            'batch_size': int(kwargs.get('num_images', 1)),
            'cfg_scale': kwargs.get('cfg_scale', 7.5),
            'seed': kwargs.get('seed', '-1'),
            'restore_faces': kwargs.get('restore_faces', False),
            'width': self.width,
            'height': self.height,
        }  # evrything that is needed for the request

    # calculates and returns a timeout based on a factor and the request data
    def _estimate_timeout(self, req_data):
        timeout = int(
            int(req_data['steps']) * int(req_data['batch_size']) * config.TIMEOUT_FACTOR)
        if req_data['restore_faces']:
            timeout = int(timeout * 1.2 * config.TIMEOUT_FACTOR)
        return timeout
