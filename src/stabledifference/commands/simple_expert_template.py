# text-to-image command
import gimpfu
import gtk
import stabledifference as sdiff
from Command import StableDiffusionCommand


class SimpleExpertCommand(StableDiffusionCommand):
    uri = "sdapi/v1/txt2img"
    metadata = StableDiffusionCommand.CommandMetadata(
        "SimpleExpertCommand",
        "StableDifference " + sdiff.__version__ + ": Simple Mode - Expert mode",
        "StableDiffusion Plugin for GIMP",
        "StableDifference",
        "StableDifference",
        "2023",
        "<Image>/StableDifference/Simple Expert Test",  # menu path
        "*", [
            #(gimpfu.PF_STRING, "prompt", "Prompt", "", ""),
            #(gimpfu.PF_SLIDER, 'steps', 'Steps', 25, (1, 150, 25)),
            #(gimpfu.PF_BOOL, 'expert', 'Show advanced options', True),
        ],
        [],
    )


"""
    def _make_request_data(self, **kwargs):
        request_data = StableDiffusionCommand._make_request_data(
            self, **kwargs)
        if kwargs['expert']:
            request_data = self._show_advanced_options(request_data)
        return request_data

    def _show_advanced_options(self, request_data):
        dialog = gtk.Dialog(title='blabla - Expert mode')
        dialog.set_border_width(10)

        sampler_index_label = gtk.Label('Sampler')
        sampler_index = gtk.combo_box_new_text()
        for sampler in sdiff.constants.SAMPLERS:
            sampler_index.append_text(sampler)
        sampler_index.set_active(0)

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

        img_target_label = gtk.Label('Results as')
        img_target = gtk.combo_box_new_text()
        for target in sdiff.constants.IMAGE_TARGETS:
            img_target.append_text(target)
        img_target.set_active(0)

        negative_prompt_label = gtk.Label('Negative Prompt')
        negative_prompt = gtk.Entry()

        seed_label = gtk.Label('Seed')
        seed = gtk.Entry()
        seed.set_text('-1')

        dialog.vbox.pack_start(sampler_index_label, True, True, 0)
        dialog.vbox.pack_start(sampler_index, True, True, 0)
        dialog.vbox.pack_start(restore_faces, True, True, 0)
        dialog.vbox.pack_start(cfg_scale_label, True, True, 0)
        dialog.vbox.pack_start(cfg_scale, True, True, 0)
        dialog.vbox.pack_start(num_images_label, True, True, 0)
        dialog.vbox.pack_start(num_images, True, True, 0)
        dialog.vbox.pack_start(img_target_label, True, True, 0)
        dialog.vbox.pack_start(img_target, True, True, 0)
        dialog.vbox.pack_start(negative_prompt_label, True, True, 0)
        dialog.vbox.pack_start(negative_prompt, True, True, 0)
        dialog.vbox.pack_start(seed_label, True, True, 0)
        dialog.vbox.pack_start(seed, True, True, 0)

        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        dialog.show_all()

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            request_data['sampler_index'] = sampler_index.get_active()
            request_data['restore_faces'] = restore_faces.get_active()
            request_data['cfg_scale'] = cfg_scale.get_value()
            request_data['num_images'] = num_images.get_value()
            request_data['img_target'] = img_target.get_active()
            request_data['negative_prompt'] = negative_prompt.get_text()
            request_data['seed'] = seed.get_text()
        dialog.destroy()
        return request_data
"""
