import os
import tempfile
from gimpfu import *
from gimpshelf import shelf
import base64

    def save_prefs(group_name, **kwargs):
        for pref_key in (key for key in kwargs.keys() if key not in ['image', 'drawable']):
            shelf[group_name + '_' + pref_key] = kwargs[pref_key]


    def encode_png(img_path):
        with open(img_path, "rb") as img:
            return 'data:image/png;base64,' + str(base64.b64encode(img.read()))


    def encode_img(img, x, y, width, height):
        img_cpy = pdb.gimp_image_duplicate(img)
        inp_layer = pdb.gimp_image_get_layer_by_name(img_cpy, constants.MASK_LAYER_NAME)
        if inp_layer:
            pdb.gimp_image_remove_layer(img_cpy, inp_layer)
        pdb.gimp_image_select_rectangle(img_cpy, 2, x, y, width, height)
        pdb.gimp_edit_copy_visible(img_cpy)
        img_flat = pdb.gimp_edit_paste_as_new_image()
        img_flat_path = tempfile.mktemp(suffix='.png')
        pdb.file_png_save_defaults(img_flat, img_flat.layers[0], img_flat_path, img_flat_path)
        encoded_img = encode_png(img_flat_path)
        # print('init img: ' + img_flat_path)
        os.remove(img_flat_path)
        return encoded_img


    def decode_png(encoded_png):
        with open(tempfile.mktemp(suffix='.png'), 'wb') as png_img:
            png_img_path = png_img.name
            png_img.write(base64.b64decode(encoded_png.split(",", 1)[0]))
            return png_img_path


    def open_images(images):
        if not images:
            return
        for encoded_img in images:
            tmp_png_path = decode_png(encoded_img)
            img = pdb.file_png_load(tmp_png_path, tmp_png_path)
            pdb.gimp_display_new(img)
            os.remove(tmp_png_path)


    def create_layers(img, layers, x, y, apply_inpainting_mask=False):
        if not layers:
            return
        inp_mask_layer = pdb.gimp_image_get_layer_by_name(img, constants.MASK_LAYER_NAME)

        def _create_nested_layers(parent_layer, layers):
            for layer in layers:
                if layer.children:
                    gimp_layer_group = pdb.gimp_layer_group_new(img)
                    gimp_layer_group.name = layer.name
                    pdb.gimp_image_insert_layer(img, gimp_layer_group, parent_layer, 0)
                    _create_nested_layers(gimp_layer_group, layer.children)
                elif layer.img:
                    tmp_png_path = decode_png(layer.img)
                    png_img = pdb.file_png_load(tmp_png_path, tmp_png_path)
                    gimp_layer = pdb.gimp_layer_new_from_drawable(png_img.layers[0], img)
                    gimp_layer.name = layer.name
                    pdb.gimp_layer_set_offsets(gimp_layer, x, y)
                    pdb.gimp_image_insert_layer(img, gimp_layer, parent_layer, 0)
                    pdb.gimp_layer_add_alpha(gimp_layer)
                    if inp_mask_layer and apply_inpainting_mask:
                        pdb.gimp_image_set_active_layer(img, gimp_layer)
                        pdb.gimp_image_select_item(img, 2, inp_mask_layer)
                        pdb.gimp_selection_invert(img)
                        pdb.gimp_edit_cut(gimp_layer)
                    pdb.gimp_image_delete(png_img)
                    os.remove(tmp_png_path)

        _create_nested_layers(parent_layer=None, layers=layers)
        pdb.gimp_selection_none(img)
        if inp_mask_layer:
            pdb.gimp_image_raise_item_to_top(img, inp_mask_layer)
            pdb.gimp_item_set_visible(inp_mask_layer, False)