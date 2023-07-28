
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
from stabledifference.constants import COLOR_SCHEME as COLORS
import gimpfu
import threading
import gtk
from gimpfu import *
import time


class StableDifferenceCommand(Thread):
    LayerResult = namedtuple('LayerResult', 'name img children')
    # CommandMetadata is just the names of the parameters of the command
    CommandMetadata = namedtuple(
        'CommandMetadata', 'proc_name, blurb, help, author, copyright, date, label, imagetypes, params, results')
    # we initialize the metadata with None, because it is set in the run_command method
    metadata = None
    command_runner = None
    name = "Name not found"
    simple_args = []
    expert_args = []

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

        # -----------------------------------------------------------------------

        def _toggle_advanced_options(self, dialog, button):
            # Toggle the visibility of the advanced options
            if button.get_label() == 'Expand':
                button.set_label('Collapse')
                _add_options(self.expert_args, dialog)
            else:
                button.set_label('Expand')
                _remove_advanced_options(self, dialog)

        def _add_options(options, dialog):
            for option in options:

                if option[0] == "STRING":
                    new_label = gtk.Label(option[2])
                    new_entry = gtk.Entry()
                    new_entry.set_name(option[1])
                    new_entry.set_text(option[3])

                    # new_label.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_entry.modify_base(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["mid"]))
                    # new_entry.modify_text(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["on_mid"]))

                    dialog.vbox.pack_start(new_label, True, True, 0)
                    dialog.vbox.pack_start(new_entry, True, True, 0)

                elif option[0] == "SLIDER":
                    new_label = gtk.Label(option[2])
                    new_slider = gtk.HScale()
                    new_slider.set_name(option[1])
                    new_slider.set_range(option[4][0], option[4][1])
                    new_slider.set_increments(option[4][2], option[4][2])
                    new_slider.set_digits(option[4][3])
                    new_slider.set_value(option[3])

                    # new_label.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_slider.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_slider.modify_base(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["mid"]))
                    # new_slider.modify_text(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["on_mid"]))
                    # new_slider.modify_cursor(gtk.gdk.color_parse(
                    #    COLORS["primary"]), gtk.gdk.color_parse("#ff0000"))

                    dialog.vbox.pack_start(new_label, True, True, 0)
                    dialog.vbox.pack_start(new_slider, True, True, 0)

                elif option[0] == "OPTION":
                    new_label = gtk.Label(option[2])
                    new_option = gtk.combo_box_new_text()
                    for label in option[4]:
                        new_option.append_text(label)
                    new_option.set_active(option[3])
                    new_option.set_name(option[1])

                    # new_label.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_option.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_option.modify_base(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["mid"]))
                    # new_option.modify_text(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["on_mid"]))
                    # new_option.modify_cursor(gtk.gdk.color_parse(
                    #    COLORS["primary"]), gtk.gdk.color_parse("#ff0000"))

                    dialog.vbox.pack_start(new_label, True, True, 0)
                    dialog.vbox.pack_start(new_option, True, True, 0)

                elif option[0] == "BOOL":
                    new_bool = gtk.CheckButton()

                    new_bool.set_label(option[2])
                    new_bool.set_name(option[1])
                    new_bool.set_active(option[3])
                    dialog.vbox.pack_start(new_label, True, True, 0)
                    dialog.vbox.pack_start(new_bool, True, True, 0)

                elif option[0] == "SPIN_BTN":
                    new_label = gtk.Label(option[2])
                    new_spinbtn = gtk.SpinButton()

                    # new_label.modify_fg(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["foreground"]))
                    # new_spinbtn.modify_base(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["mid"]))
                    # new_spinbtn.modify_text(
                    #    gtk.STATE_NORMAL, gtk.gdk.color_parse(COLORS["on_mid"]))
                    # new_spinbtn.modify_cursor(gtk.gdk.color_parse(
                    #    COLORS["primary"]), gtk.gdk.color_parse("#ff0000"))

                    new_spinbtn.set_name(option[1])
                    new_spinbtn.set_range(option[4][0], option[4][1])
                    new_spinbtn.set_increments(option[4][2], option[4][2])
                    new_spinbtn.set_value(option[3])
                    dialog.vbox.pack_start(new_label, True, True, 0)
                    dialog.vbox.pack_start(new_spinbtn, True, True, 0)

            dialog.show_all()

        # removes the advanced options from the dialog, and saves the values of the options temporarily
        def _remove_advanced_options(self, dialog):
            expert_options = self.expert_args
            for i in range(len(expert_options)):
                option = expert_options[i]
                for widget in dialog.vbox.get_children():
                    if isinstance(widget, gtk.Label) and widget.get_text() == option[2]:
                        widget.destroy()
                    elif isinstance(widget, gtk.HScale) and widget.get_name() == option[1]:
                        self.expert_args[i] = (
                            option[0], option[1], option[2], widget.get_value(), option[4])
                        widget.destroy()
                    elif isinstance(widget, gtk.CheckButton) and widget.get_name() == option[1]:
                        self.expert_args[i] = (
                            option[0], option[1], option[2], widget.get_active())
                        widget.destroy()
                    elif isinstance(widget, gtk.SpinButton) and widget.get_name() == option[1]:
                        self.expert_args[i] = (
                            option[0], option[1], option[2], widget.get_value(), option[4])
                        widget.destroy()
                    elif isinstance(widget, gtk.ComboBox) and widget.get_name() == option[1]:
                        self.expert_args[i] = (
                            option[0], option[1], option[2], widget.get_active(), option[4])
                        widget.destroy()
                    elif isinstance(widget, gtk.Entry) and widget.get_name() == option[1]:
                        self.expert_args[i] = (
                            option[0], option[1], option[2], widget.get_text())
                        # update the value of the expert_args

                        widget.destroy()
            # resize the dialog to fit the new content just added
            dialog.resize(1, 1)

            dialog.show_all()

        def get_kwargs(dialog):
            kwargs = {}
            for widget in dialog.vbox.get_children():
                if isinstance(widget, gtk.HScale):
                    kwargs.update({widget.get_name(): widget.get_value()})
                elif isinstance(widget, gtk.CheckButton):
                    kwargs.update({widget.get_label(): widget.get_active()})
                elif isinstance(widget, gtk.SpinButton):
                    kwargs.update({widget.get_name(): widget.get_value()})
                elif isinstance(widget, gtk.ComboBox):
                    kwargs.update({widget.get_name(): widget.get_active()})
                elif isinstance(widget, gtk.Entry):
                    kwargs.update({widget.get_name(): widget.get_text()})
            return kwargs

        # -----------------------------------------------------------------------
        #gtk.settings_get_default().set_string_property('gtk-theme-name', 'Dark', '')
        # Create a new GTK dialog
        dialog = gtk.Dialog(title=self.name)
        dialog.present()

        dialog.set_border_width(10)
        # dialog.modify_bg(gtk.STATE_NORMAL,
        #                 gtk.gdk.color_parse(COLORS["background"]))

        #style_provider = gtk.CssProvider()
        # style_provider.load_from_path("style.css")

        simple_options = self.simple_args
        _add_options(simple_options, dialog)

        # Create a new GTK button to show/hide the advanced options
        if self.expert_args:
            advanced_button = gtk.Button(label='Expand')
            advanced_button.connect(
                'clicked', lambda button: _toggle_advanced_options(self, dialog, advanced_button))
            dialog.vbox.pack_start(advanced_button, True, True, 0)

        # Add the OK and Cancel buttons to the dialog
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        #progress_bar = gtk.ProgressBar()
        # progress_bar.set_fraction(0.0)
        # progress_bar.set_text("Processing...")
        # progress_bar.set_pulse_step(0.01)
        #dialog.vbox.pack_end(progress_bar, True, True, 0)

        # Show the dialog
        dialog.show_all()

        # Run the dialog and get the response
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            kwargs.update({'image': image, 'drawable': drawable})
            kwargs.update(get_kwargs(dialog))

        dialog.destroy()

        # call the run_command function
        self.command_runner(self(**kwargs))
        #self.run_command(self, image, drawable, request_data)

        # dialog.destroy()

    # -----------------------------------------------------------------------


class StableDiffusionCommand(StableDifferenceCommand):
    uri = ''

    def __init__(self, **kwargs):
        StableDifferenceCommand.__init__(self, **kwargs)
        self.url = urljoin(sdiff.gimp.pref_value(
            PREFS, 'api_base_url', sdiff.constants.DEFAULT_API_URL), self.uri)  # api URL TODO shelf url aus settings?
        self.img = kwargs['image']  # image to be processed
        self.images = None  # images to be processed
        self.layers = None  # layers to be processed
        self.uncrop = False

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

            # create the request
            self.sd_request = Request(url=self.url,
                                      headers={
                                          'Content-Type': 'application/json'},
                                      data=json.dumps(self.req_data))  # request data

            # start it in a parallel thread
            thread = threading.Thread(target=self.start_request)
            thread.start()
            thread.join()

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
            # TODO self._post_process()

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
        }  # evrything that is needed for the request

    # calculates and returns a timeout based on a factor and the request data
    def _estimate_timeout(self, req_data):
        timeout = int(
            int(req_data['steps']) * int(req_data['batch_size']) * config.TIMEOUT_FACTOR)
        if req_data['restore_faces']:
            timeout = int(timeout * 1.2 * config.TIMEOUT_FACTOR)
        return timeout

    # resize (enlarge) the canvas by the padding
    def _resize_canvas(self, **kwargs):
        pad_left = kwargs.get('padding_left', 128)
        pad_right = kwargs.get('padding_right', 128)
        pad_top = kwargs.get('padding_top', 128)
        pad_btm = kwargs.get('padding_bottom', 128)

        # resize canvas
        new_width = self.width + pad_left + pad_right
        new_height = self.height + pad_top + pad_btm

        x = pad_left
        y = pad_top

        pdb.gimp_image_resize(self.img, new_width, new_height, x, y)
        for layer in self.img.layers:
            pdb.gimp_layer_resize_to_image_size(layer)

    def _rescale_uncrop(self, layers_names):
        translate_x = self.padding - self.padding_left if self.padding_left > 0 else 0
        translate_y = self.padding - self.padding_top if self.padding_top > 0 else 0

        for layer_name in layers_names:
            #layer = pdb.gimp_image_get_layer_by_name(self.img, layer_name)
            pdb.gimp_layer_translate(pdb.gimp_image_get_layer_by_name(
                self.img, layer_name), -translate_x, -translate_y)
            pdb.gimp_layer_resize_to_image_size(
                pdb.gimp_image_get_layer_by_name(self.img, layer_name))
