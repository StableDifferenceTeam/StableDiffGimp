#!/usr/bin/python

import gtk
import gimpfu


def _toggle_advanced_options(dialog, button):
    # Toggle the visibility of the advanced options
    if button.get_label() == 'Expand':
        button.set_label('Collapse')
        _add_advanced_options(dialog)
    else:
        button.set_label('Expand')
        _remove_advanced_options(dialog)


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
