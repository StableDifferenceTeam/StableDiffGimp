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
import gimpfu
import gtk
from gimpfu import *
import time
import os


class StableDifferenceCommand(Thread):
    LayerResult = namedtuple('LayerResult', 'name img children')
    # CommandMetadata is a named tuple that contains everything that is needed to register a command in gimp
    # except the function that is called when the command is executed
    CommandMetadata = namedtuple(
        'CommandMetadata', 'proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results')
    # we initialize the metadata with None, because it is set in the run_command method
    metadata = None
    command_runner = None
    # name of the Command, shows up as title of the gtk dialog
    name = "Name not found"
    # simple_args are the arguments that are shown in the gtk dialog by default
    simple_args = []
    # expert_args are the arguments that are shown in the gtk dialog when the user clicks on "Expand"
    expert_args = []
    # args are of shape
    """[
    ('STRING', 'identifier', 'Label', 'Default value'),
    ('OPTION', 'identifier', 'Label', int(Default Index) , List(possible values)),
    ('BOOL', 'identifier', 'Label', bool(Default value)),
    ('SLIDER', 'identifier', 'Label', float(Default value), (float(min), float(max), float(step), int(decimal point count))),
    ('SPIN_BTN', 'identifier', 'Label', int(Default value), (int(min), int(max), int(step)))
    ]"""

    @classmethod
    def run_command(cls, *args, **kwargs):
        # args is the actual parameters of the command, kwargs is where the parameters are stored in named variables
        kwargs.update(
            dict(zip((param[1] for param in cls.metadata.params), args)))
        cls.command_runner(cls(**kwargs))

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.status = 'INITIALIZED'

    # ----------------------gtk dialog methods----------------------------------

    @classmethod
    def _open_gtk_options(self, image, drawable, **kwargs):
        # ----------------------inner gtk methods-------------------------------

        def _toggle_advanced_options(self, dialog, button):
            # Toggle the visibility of the advanced options
            if button.get_label() == 'Expand':
                button.set_label('Collapse')
                _add_options(self.expert_args, dialog)
            else:
                button.set_label('Expand')
                _remove_advanced_options(self, dialog)

        # add options to the dialog, used for simple and expert options
        def _add_options(options, dialog):
            for option in options:
                if option[0] == "STRING":
                    hbox = gtk.HBox(True, 10)
                    new_label = gtk.Label(option[2])
                    new_entry = gtk.Entry()
                    new_entry.set_name(option[1])
                    new_entry.set_text(option[3])
                    hbox.pack_start(new_label, False, False, 5)
                    hbox.pack_start(new_entry, True, True, 0)
                    hbox.set_child_packing(
                        new_label, True, True, 0, gtk.PACK_START)
                    new_label.set_alignment(0, 0.5)
                    dialog.vbox.pack_start(hbox, True, True, 0)

                elif option[0] == "SLIDER":
                    hbox = gtk.HBox(True, 10)
                    new_label = gtk.Label(option[2])
                    new_slider = gtk.HScale()
                    new_slider.set_name(option[1])
                    new_slider.set_range(option[4][0], option[4][1])
                    new_slider.set_increments(option[4][2], option[4][2])
                    new_slider.set_digits(option[4][3])
                    new_slider.set_value(option[3])
                    hbox.pack_start(new_label, False, False, 5)
                    hbox.pack_start(new_slider, True, True, 0)
                    hbox.set_child_packing(
                        new_label, True, True, 0, gtk.PACK_START)
                    new_label.set_alignment(0, 0.5)
                    dialog.vbox.pack_start(hbox, True, True, 0)

                elif option[0] == "OPTION":
                    hbox = gtk.HBox(True, 10)
                    new_label = gtk.Label(option[2])
                    new_option = gtk.combo_box_new_text()
                    for label in option[4]:
                        new_option.append_text(label)
                    new_option.set_active(option[3])
                    new_option.set_name(option[1])
                    hbox.pack_start(new_label, False, False, 0)
                    hbox.pack_start(new_option, True, True, 0)
                    hbox.set_child_packing(
                        new_label, True, True, 0, gtk.PACK_START)
                    new_label.set_alignment(0, 0.5)
                    dialog.vbox.pack_start(hbox, True, True, 0)

                elif option[0] == "BOOL":
                    hbox = gtk.HBox(True, 10)
                    new_label = gtk.Label(option[2])
                    new_bool = gtk.Button(label=option[3])
                    new_bool.set_name(option[1])
                    new_bool.connect(
                        "clicked", lambda button: _toggle_bool(button))
                    hbox.pack_start(new_label, False, False, 5)
                    hbox.pack_end(new_bool, False, False, 0)
                    hbox.set_child_packing(
                        new_label, True, True, 0, gtk.PACK_START)
                    hbox.set_child_packing(
                        new_bool, True, True, 0, gtk.PACK_END)
                    new_label.set_alignment(0, 0.5)
                    dialog.vbox.pack_start(hbox, True, True, 0)

                elif option[0] == "SPIN_BTN":
                    hbox = gtk.HBox(True, 10)
                    new_label = gtk.Label(option[2])
                    new_spinbtn = gtk.SpinButton()
                    new_spinbtn.set_name(option[1])
                    new_spinbtn.set_range(option[4][0], option[4][1])
                    new_spinbtn.set_increments(option[4][2], option[4][2])
                    new_spinbtn.set_value(option[3])
                    hbox.pack_start(new_label, False, False, 0)
                    hbox.pack_start(new_spinbtn, True, True, 0)
                    hbox.set_child_packing(
                        new_label, True, True, 0, gtk.PACK_START)
                    new_label.set_alignment(0, 0.5)
                    dialog.vbox.pack_start(hbox, True, True, 0)
            dialog.show_all()

            def _toggle_bool(button):
                if button.get_label() == 'True':
                    button.set_label('False')
                else:
                    button.set_label('True')

        # removes the advanced options from the dialog, and saves the values of the options temporarily
        def _remove_advanced_options(self, dialog):
            # list of advanced options
            expert_options = self.expert_args
            for i in range(len(expert_options)):
                option = expert_options[i]

                for hbox in dialog.vbox.get_children():
                    # check for type of widget and name of widget
                    # and if it matches, save its value into expert args of the widget and destroy it
                    # this way, when you input advanced options, collapse and advance, the values are saved
                    for widget in hbox.get_children():
                        if isinstance(widget, gtk.HScale) and widget.get_name() == option[1]:
                            self.expert_args[i] = (
                                option[0], option[1], option[2], widget.get_value(), option[4])
                            hbox.destroy()
                        elif isinstance(widget, gtk.Button) and widget.get_name() == option[1]:
                            self.expert_args[i] = (
                                option[0], option[1], option[2], widget.get_label())
                            hbox.destroy()
                        elif isinstance(widget, gtk.SpinButton) and widget.get_name() == option[1]:
                            self.expert_args[i] = (
                                option[0], option[1], option[2], widget.get_value(), option[4])
                            hbox.destroy()
                        elif isinstance(widget, gtk.ComboBox) and widget.get_name() == option[1]:
                            self.expert_args[i] = (
                                option[0], option[1], option[2], widget.get_active(), option[4])
                            hbox.destroy()
                        elif isinstance(widget, gtk.Entry) and widget.get_name() == option[1]:
                            self.expert_args[i] = (
                                option[0], option[1], option[2], widget.get_text())
                            hbox.destroy()

            # resize the dialog to the minimum size
            dialog.resize(1, 1)

            dialog.show_all()

        # saves the values of the dialog into a dictionary
        def get_kwargs(dialog):
            kwargs = {}
            for hbox in dialog.vbox.get_children():
                for widget in hbox.get_children():
                    if isinstance(widget, gtk.HScale):
                        kwargs.update({widget.get_name(): widget.get_value()})
                    elif isinstance(widget, gtk.Button):
                        kwargs.update(
                            {widget.get_name(): True if widget.get_label() == 'True' else False})
                    elif isinstance(widget, gtk.SpinButton):
                        kwargs.update({widget.get_name(): widget.get_value()})
                    elif isinstance(widget, gtk.ComboBox):
                        kwargs.update({widget.get_name(): widget.get_active()})
                    elif isinstance(widget, gtk.Entry):
                        kwargs.update({widget.get_name(): widget.get_text()})
            return kwargs

        # -------------------------inner functions end--------------------------
        # Create a new GTK dialog and set its Name
        dialog = gtk.Dialog(title=self.name)
        dialog.present()
        dialog.set_size_request(500, -1)
        dialog.set_border_width(10)
        dialog.vbox.set_spacing(3)

        style_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "style")
        #dialog.set_title(str(assets_path))
        gtk.rc_parse(os.path.join(style_path, "dark_mode_style"))

        # add the simple options to the dialog (minimum required options)
        simple_options = self.simple_args
        _add_options(simple_options, dialog)

        # Create a new GTK button to show/hide the advanced options in case they are not empty
        if self.expert_args:
            advanced_button = gtk.Button(label='Expand')
            # make the button size as small to only fit the text
            advanced_button.connect(
                'clicked', lambda button: _toggle_advanced_options(self, dialog, advanced_button))
            dialog.vbox.pack_start(advanced_button, True, True, 0)

        # Add the OK and Cancel buttons to the dialog
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        # Show the dialog
        dialog.show_all()

        # Run the dialog and get the response
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            kwargs.update({'image': image, 'drawable': drawable})
            kwargs.update(get_kwargs(dialog))

        dialog.destroy()

        # call the run_command function to run the command with the given arguments
        self.command_runner(self(**kwargs))

    # ---------------------------gtk dialog end---------------------------------


class StableDiffusionCommand(StableDifferenceCommand):
    uri = ''
    api_url = ''

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(os.path.dirname(os.path.dirname(path)))

    # check if settings.json exists, if not, create it and add the default api url
    if not os.path.isfile(os.path.join(path, "settings.json")):
        print("settings.json does not exist")
        with open(os.path.join(path, "settings.json"), 'w') as f:
            json.dump({
                "api_base_url": sdiff.constants.DEFAULT_API_URL,
                "styling": "Dark Mode"
                       }, f)

    # read the api url from the settings.json file
    with open(os.path.join(path, "settings.json"), 'r') as f:
        settings = json.load(f)
        api_url = settings['api_base_url']
        styling = settings['styling']
    
    # set the styling
    if styling != "None":
        style_path = os.path.join(path, "src", "style")
        gtk.rc_parse(os.path.join(style_path, styling.replace(" ", "_")))

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)

        self.url = urljoin(self.api_url, self.uri)
        self.img = kwargs['image']  # image to be processed
        self.images = None  # images to be processed
        self.layers = None  # layers to be processed
        self.uncrop = False  # wether it is a uncrop request or not

        self.x, self.y, self.width, self.height = self._determine_active_area()  # selected area

        print('x, y, w, h: ' + str(self.x) + ', ' + str(self.y) +
              ', ' + str(self.width) + ', ' + str(self.height))

        self.img_target = sdiff.constants.IMAGE_TARGETS[kwargs.get(
            'img_target', 0)]  # layers are the default img_target

        self.req_data = self._make_request_data(**kwargs)
        if config.TIMEOUT_REQUESTS:
            self.timeout = self._estimate_timeout(self.req_data)
        else:
            self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT  # type: ignore

    # the method conducting the request
    def start_request(self):
        try:
            self.sd_resp = urlopen(self.sd_request, timeout=self.timeout)
        except Exception as e:
            self.error_msg = str(e)
            self.status = 'ERROR'

    def run(self):
        self.status = 'RUNNING'

        try:
            # prints out a request path
            if config.LOG_REQUESTS:
                req_path = tempfile.mktemp(prefix='req_', suffix='.json')
                with open(req_path, 'w') as req_file:
                    print('request: ' + req_path)
                    req_file.write(json.dumps(self.req_data))

            # create the request data in json format
            self.sd_request = Request(url=self.url,
                                      headers={
                                          'Content-Type': 'application/json'},
                                      data=json.dumps(self.req_data))  # request data

            self.sd_resp = urlopen(self.sd_request, timeout=self.timeout)

            # if it failed for some reason
            if self.status == 'ERROR':
                print("ERROR while conducting the request:")
                print(self.error_msg)
                gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CANCEL,
                                  "An error occurred while calling the generative model:\n"+str(self.error_msg)).run()

            else:
                if self.sd_resp:
                    self.response = json.loads(
                        self.sd_resp.read())  # read response
                    if config.LOG_REQUESTS:
                        # create temporary response file
                        resp_path = tempfile.mktemp(
                            prefix='resp_', suffix='.json')
                        with open(resp_path, 'w') as resp_file:  # write response to file
                            print('response: ' + resp_path)
                            resp_file.write(json.dumps(self.response))

                # process response (see below)
                self._process_response(self.response)
            self.status = 'DONE'

        except Exception as e:  # catch ERROR

            print("command exception:")
            self.error_msg = str(e)
            print(e)
            self.status = 'ERROR'

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
        # get the kwargs, if not set, use default values
        return {
            'prompt': kwargs.get('prompt', ''),
            'negative_prompt': kwargs.get('negative_prompt', ''),
            'steps': int(kwargs.get('steps', 25)),
            'sampler_index': sdiff.constants.SAMPLERS[kwargs.get('sampler_index', 0)],
            'batch_size': int(kwargs.get('num_images', 1)),
            'cfg_scale': kwargs.get('cfg_scale', 7.5),
            'seed': kwargs.get('seed', '-1'),
            'restore_faces': kwargs.get('restore_faces', False),
            'width': self.width,
            'height': self.height,
        }  # everything that is needed for the request

    # calculates and returns a timeout based on a factor and the request data
    def _estimate_timeout(self, req_data):
        timeout = int(
            int(req_data['steps']) * int(req_data['batch_size']) * config.TIMEOUT_FACTOR)
        if req_data['restore_faces']:
            timeout = int(timeout * 1.2 * config.TIMEOUT_FACTOR)
        return timeout

    # resize (enlarge) the canvas by the padding
    def _resize_canvas(self, **kwargs):
        # default is 128
        pad_left = kwargs.get('padding_left', 128)
        pad_right = kwargs.get('padding_right', 128)
        pad_top = kwargs.get('padding_top', 128)
        pad_btm = kwargs.get('padding_bottom', 128)

        # resize canvas
        new_width = self.width + pad_left + pad_right
        new_height = self.height + pad_top + pad_btm

        x = pad_left
        y = pad_top
        # place image according to padding
        pdb.gimp_image_resize(self.img, new_width, new_height, x, y)
        for layer in self.img.layers:
            pdb.gimp_layer_resize_to_image_size(layer)

    def _rescale_uncrop(self, layers_names):
        translate_x = self.padding - self.padding_left if self.padding_left > 0 else 0
        translate_y = self.padding - self.padding_top if self.padding_top > 0 else 0

        for layer_name in layers_names:
            # translate the layers so the desired part is in the image
            pdb.gimp_layer_translate(pdb.gimp_image_get_layer_by_name(
                self.img, layer_name), -translate_x, -translate_y)
            # crop the layers to the desired size
            pdb.gimp_layer_resize_to_image_size(
                pdb.gimp_image_get_layer_by_name(self.img, layer_name))
