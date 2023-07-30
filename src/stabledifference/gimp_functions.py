import os
import tempfile
from gimpfu import *
import base64
import constants

# encodes a png image to base64


def encode_png(img_path):
    with open(img_path, "rb") as img:
        # base64 encodes 8-bit binary data
        return 'data:image/png;base64,' + str(base64.b64encode(img.read()))


# encodes an image
def encode_img(img, x, y, width, height):
    # copy the image
    img_cpy = pdb.gimp_image_duplicate(img)

    # get the 'Inpainting Maks' layer
    inp_layer = pdb.gimp_image_get_layer_by_name(
        img_cpy, constants.MASK_LAYER_NAME)
    # if an inpainting mask exists, remove it from the image
    if inp_layer:
        pdb.gimp_image_remove_layer(img_cpy, inp_layer)

    # select the rectangle (necessary for text to image)
    pdb.gimp_image_select_rectangle(img_cpy, 2, x, y, width, height)

    # flatten the image
    pdb.gimp_edit_copy_visible(img_cpy)
    img_flat = pdb.gimp_edit_paste_as_new_image()
    img_flat_path = tempfile.mktemp(suffix='.png')
    pdb.file_png_save_defaults(
        img_flat, img_flat.layers[0], img_flat_path, img_flat_path)
    # and encode it
    encoded_img = encode_png(img_flat_path)
    # remove the temporary image
    os.remove(img_flat_path)

    return encoded_img


# gets the active area of the image
# the active area is the area you select to work on
def active_area(img):
    _, x, y, x2, y2 = pdb.gimp_selection_bounds(img)
    return x, y, x2 - x, y2 - y


def autofit_inpainting_area(img):
    # raise an exception if there is no 'Inpainting Mask' layer available
    if not pdb.gimp_image_get_layer_by_name(img, constants.MASK_LAYER_NAME):
        raise Exception("Couldn't find layer named '" +
                        constants.MASK_LAYER_NAME + "'")

    img_cpy = pdb.gimp_image_duplicate(img)
    mask_layer = pdb.gimp_image_get_layer_by_name(
        img_cpy, constants.MASK_LAYER_NAME)
    # need to make it the active layer ...
    pdb.gimp_image_set_active_layer(img_cpy, mask_layer)
    # ... because this unintuitively crops the active layer (!)
    pdb.plug_in_autocrop_layer(img_cpy, mask_layer)
    # calculate width and height
    # the width and height of the inpainting area should be 256 or 512
    target_width = math.ceil(float(mask_layer.width) / 256) * 256
    target_width = max(512, target_width)
    target_height = math.ceil(float(mask_layer.height) / 256) * 256
    target_height = max(512, target_height)
    # calculate x and y
    mask_center_x = mask_layer.offsets[0] + int(mask_layer.width / 2)
    mask_center_y = mask_layer.offsets[1] + int(mask_layer.height / 2)
    x, y = mask_center_x - target_width / 2, mask_center_y - target_height / 2
    if x + target_width > img_cpy.width:
        x = img_cpy.width - target_width
    if y + target_height > img_cpy.height:
        y = img_cpy.height - target_height
    if mask_center_x - target_width / 2 < 0:
        x = 0
    if mask_center_y - target_height / 2 < 0:
        y = 0
    return x, y, target_width, target_height


def encode_mask(img, x, y, width, height):
    # raise an exception if there is no 'Inpainting Mask' layer available
    if not pdb.gimp_image_get_layer_by_name(img, constants.MASK_LAYER_NAME):
        raise Exception("Couldn't find layer named '" +
                        constants.MASK_LAYER_NAME + "'")

    # creates a duplicate of an image
    img_cpy = pdb.gimp_image_duplicate(img)
    for layer in img_cpy.layers:
        # set only the inpainting mask layer visible
        pdb.gimp_item_set_visible(
            layer, layer.name == constants.MASK_LAYER_NAME)

    # feather the selection for a smoother inpainting
    pdb.gimp_context_set_feather(True)
    pdb.gimp_context_set_feather_radius(10, 10)

    # select the rectangle and encode it
    pdb.gimp_image_select_rectangle(img_cpy, 2, x, y, width, height)
    pdb.gimp_edit_copy_visible(img_cpy)
    mask_img = pdb.gimp_edit_paste_as_new_image()
    pdb.gimp_layer_flatten(mask_img.layers[0])

    mask_img_path = tempfile.mktemp(suffix='.png')
    pdb.file_png_save_defaults(
        mask_img, mask_img.layers[0], mask_img_path, mask_img_path)
    encoded_mask = encode_png(mask_img_path)
    # remove the temporary image
    os.remove(mask_img_path)
    return encoded_mask


# decode the previously encoded image and save it as a temporary file
def decode_png(encoded_png):
    with open(tempfile.mktemp(suffix='.png'), 'wb') as png_img:
        png_img_path = png_img.name
        png_img.write(base64.b64decode(encoded_png.split(",", 1)[0]))
        return png_img_path


# open the images in gimp
def open_images(images):
    if not images:
        return
    for encoded_img in images:
        tmp_png_path = decode_png(encoded_img)
        img = pdb.file_png_load(tmp_png_path, tmp_png_path)
        pdb.gimp_display_new(img)
        os.remove(tmp_png_path)


# creates layers
def create_layers(img, layers, x, y, apply_inpainting_mask=False):
    if not layers:
        return
    # get the inpainting mask layer
    inp_mask_layer = pdb.gimp_image_get_layer_by_name(
        img, constants.MASK_LAYER_NAME)

    # initialize the list of layers names
    layers_names = []

    # creates parent and child layers (nested)
    def _create_nested_layers(parent_layer, layers, layers_names):
        for layer in layers:
            # if the layer has children, create a layer group
            if layer.children:
                gimp_layer_group = pdb.gimp_layer_group_new(img)
                gimp_layer_group.name = layer.name
                # save the layer name
                layers_names.append(layer.name)
                pdb.gimp_image_insert_layer(
                    img, gimp_layer_group, parent_layer, 0)
                # recursively create the children layers
                _create_nested_layers(
                    gimp_layer_group, layer.children, layers_names)
            # if the layer has an image, create a layer
            elif layer.img:
                tmp_png_path = decode_png(layer.img)
                png_img = pdb.file_png_load(tmp_png_path, tmp_png_path)
                gimp_layer = pdb.gimp_layer_new_from_drawable(
                    png_img.layers[0], img)
                gimp_layer.name = layer.name
                # save the layer name
                layers_names.append(layer.name)
                pdb.gimp_layer_set_offsets(gimp_layer, x, y)
                pdb.gimp_image_insert_layer(img, gimp_layer, parent_layer, 0)
                pdb.gimp_layer_add_alpha(gimp_layer)
                if inp_mask_layer and apply_inpainting_mask:
                    # crop the layer to the inpainting mask
                    pdb.gimp_image_set_active_layer(img, gimp_layer)
                    pdb.gimp_image_select_item(img, 2, inp_mask_layer)
                    pdb.gimp_selection_invert(img)
                    pdb.gimp_edit_cut(gimp_layer)
                pdb.gimp_image_delete(png_img)
                os.remove(tmp_png_path)
        return layers_names

    # When no parent layer exists, get the mask layer to the top
    if type(layers) == list:
        layers_names = _create_nested_layers(
            parent_layer=None, layers=layers, layers_names=layers_names)
    else:
        layers_names = _create_nested_layers(parent_layer=None, layers=[
                                             layers], layers_names=layers_names)
    pdb.gimp_selection_none(img)
    # if the inpainting mask layer exists, set it to the top and hide it
    if inp_mask_layer:
        pdb.gimp_image_raise_item_to_top(img, inp_mask_layer)
        pdb.gimp_item_set_visible(inp_mask_layer, False)

    return layers_names
