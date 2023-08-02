# StableDiffGimp
## Description
***
This is a plugin for GIMP that allows you to incorporate Stable Diffusion into your workflow. It is based on the [AUTOMATIC1111's Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).


## Installation
***
1. Download GIMP or verify, that you own the newest version of GIMP. 
2. Clone [The Stable Diff Gimp Repository] (https://github.com/PeterIsbrandt/StableDiffGimp.git) by typing `git clone https://github.com/PeterIsbrandt/StableDiffGimp.git` in your terminal.
3. Go to GIMP and add the Plugin to the list of plugins:
    - Open GIMP
    - Click on `Settings`
    - Click on `Folder`
    - Click on `Plugins`
    - Click on `Add a new folder`
    - Type in the location of your StableDiffGimp **src** folder. It should look something like: `/Users/.../StableDiffGimp/src`
    - Close GIMP
    - Open it again and verify, that you have a StableDifference button
4. Start Stable Diffusion
    - You can start it on your own PC. If you do that, in the settings should be: `API BASE URL`
5. Have fun using StableDifference!


## Simple Mode vs. Expert Mode
***
If you are a new user without much knowledge about Stable Diffusion or GIMP, consider using **Simple Mode**.
If you want lots of customizability, try using **Expert Mode**.
Most our features exist in an Expert and a Simple Mode.


## Settings 
***
1. Click on `StableDifference`, then `Settings`
2. A new window should open up, where you can add an API url (for example from a Colab)


## Our features
***
- Before getting started, please note that some of the buttons are greyed out before adding an image or a new canvas
- To add an image, you can use drag and drop
- To add a new canvas, click on `File`, then `New`


### Image to Image
- modifies an existing image
- Exists in Simple and Expert Mode

#### Simple Mode

#### Expert Mode


### Inpainting
- Paints a new picture inside an existing picture
- Exists in Simple and Expert Mode

#### Simple Mode


#### Expert Mode


### Text to Image
- Creates a new image from a prompt
- Exists in Simple and Expert Mode

#### Simple Mode
1. Click on `StableDifference`, then `Text to Image`, then `Simple Mode`
2. A window should open up
3. On top is a prompt. You can write anything in there and the Plugin will use this prompt to create an Image
4. Click on `Ok`
5. You created an image by text!

#### Expert Mode
1. Click on `StableDifference`, then `Text to Image`, then `Expert Mode`
2. A window should open up
3. On top is a prompt. You can write anything in there and the Plugin will use this prompt to create an Image
4. Below the prompt, you have a couple more options to costumize the result even more
5. Click on `Ok`
6. You created an image by text!


### Uncrop
- Crops an existing image to a variable size

1. Insert an existing picture into your GIMP
2. Click on `StableDifference`, then `Uncrop`, then `Simple Mode`
3. A window should open up
4. On top is a prompt. You can write anything in there and the Plugin will add it in the uncropped space
5. You can see different sliders for padding on the top, bottom, left and right 
6. The number on top of each slider tells you how much you uncrop on the according side of the image
7. The `steps` slider on the bottom lets you choose in how many steps the prompt and the uncropping is completed. More steps = a more defined image
8. If you have settled on a number, click on `Ok`
9. The image is now uncropped!












