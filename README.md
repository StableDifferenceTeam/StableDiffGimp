# StableDifference
## Description
***
This is a plugin for GIMP that allows you to incorporate Stable Diffusion into your workflow. It is based on the [AUTOMATIC1111's Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).


## Installation
***
1. Download GIMP or verify, that you own the newest version of GIMP
2. Clone [The Stable Diff Gimp Repository] (https://github.com/StableDifferenceTeam/StableDiffGimp.git) by typing `git clone https://github.com/StableDifferenceTeam/StableDiffGimp.git` in your terminal
3. Go to GIMP and add the Plugin to the list of plugins:
    - Open GIMP
    - Click on `Settings`
    - Click on `Folder`
    - Click on `Plugins`
    - Click on `Add a new folder`
    - Type in the location of your StableDiffGimp **src** folder. It should look something like: **/Users/.../StableDiffGimp/src**
    - Close GIMP
    - Open it again and verify, that you have a StableDifference button
4. Start Stable Diffusion
    - You can start it on your own PC. If you do that, in the settings should be: `http://localhost:7860`
5. Have fun using StableDifference!


## Simple or more advanced?
***
Each of our features has a drop-down menu, so if you are a user with vast knowledge or you seek more customizability, click on `Expand`
You find an explanation of what each setting does [here](##what-does-each-setting-do?)


## Settings 
***
1. Click on `StableDifference`, then `Settings`
2. A new window should open up, where you can add an API url
	- The default URL is `http://localhost:7860 `(which is your computer)
3. Choose if you want to use our prompt generator
	- A prompt generator helps you to choose a prompt
4. In a drop-down menu below, you can choose between Dark Mode, Light Mode or None for your pop-up windows
	- Dark Mode lets all of the pop-up windows appear in a dark theme, light mode in light and none in a classic theme


## Our features
***
- Before getting started, please note that all of the buttons are greyed out before adding an image or a new canvas
	- To add an image, you can use drag and drop
	- To add a new canvas, click on `File`, then `New`
- Overview:
	- [Image to Image](###image-to-image)
	- [Inpainting](###inpainting)
	- [Text to Image](###text-to-image)
	- [Uncrop](###uncrop)
	- [Upscale](###upscale)
- Depending on the step number and other factors, it may take some time to create an image. To make your wait time sweeter, we created some cute messages for you:


### Image to Image
Modifies an existing image

1. Make sure you have an image in your GIMP
2. Click on `StableDifference`, then `Image to Image`
3. A window should open up with a [prompt](####prompt), a [denoising strength](####denoising-strength) and a drop-down menu
	- Click on expand to customize further
	- [Here](###expandable-menu) are our advanced options
4. Choose your input and click on `Ok`
5. You modified your image!


### Inpainting
Paints a new image inside an existing image

1. Make sure you have an image in your GIMP
2. Create a new layer and call it `Inpainting Mask`
3. Mark the area you want the prompt to appear in
4. Click on `StableDifference`, then `Inpainting`
5. A window should open up 
6. Write a [prompt](####prompt), choose a [denoising strength](####denoising-strength) and [steps](####steps)
	- Click on expand to customize further
	- [Here](###expandable-menu) are our advanced options
7. Choose your input and click on `Ok`
8. You modified your image!


### Text to Image
Creates a new image from a prompt

1. Click on `StableDifference`, then `Text to Image`
2. A window should open up
3. Write a [prompt](####prompt) and choose [steps](####steps)
	- Click on expand to customize further
	- [Here](###expandable-menu) are our advanced options
4. Click on `Ok`
5. You created an image by text!


### Uncrop
Uncrops an existing image to a variable size and adds a prompt

1. Insert an existing picture into your GIMP
2. Click on `StableDifference`, then `Uncrop`
3. A window should open up
4. Write a [prompt](####prompt)
5. You can see different sliders for padding on the top, bottom, left and right 
	- Each slider lets you choose how much space you add on the according side
6. Choose in how many [steps](####steps) you want your image to be completed
7. If you have settled on a number, click on `Ok`
8. The image is now uncropped!


### Upscale
Makes an image higher-defined

1. Insert an existing picture into your GIMP
2. Click on `StableDifference`, then `Upscale`
3. A window should open up
4. Choose an [upscaling factor](####upscaling-factor)
5. If you have settled on a number, click on `Ok`
6. The image is now upscaled!


## What does each setting do?
***
#### Prompt
- In textform, write what you want to generate

#### Denoising strength
- The higher the denoising strength, the less the output image will look like the input image

#### Steps
- The more steps, the more definition

#### Upscaling Factor
- How much the image will be upscaled
    - The higher the number, the more upscaling it will have


------------

## Expandable menu
***
#### Negative Prompt
- What you do not want your image to include 

#### Seed
- Is a number from which Stable Diffusion adds noise to the picture

#### Sampler
- A sampler creates a clear picture from noise
- We have multiple samplers to choose from

#### Restore faces
- If you set it on `True` you can fill in missing or distorted parts of a face 

#### CFG
- Means Classifier Free Guidance scale
- The higher the number, the more closely Stable Diffusion follows your prompt

#### Number of Images
- How many images you want to create

#### Results as 
- If you want your result to be a layer in your GIMP or an image

***
The following settings are just for inpainting

#### Inpainting fill
- How the Inpainting Mask is initialized
- You can choose between four options

#### Inpaint at full resolution
- If you set it on `True`, you will inpaint at full resolution

#### Full resolution Inpaint padding
- Set a padding for your inpainting with the slider
	- 0 means no padding

#### Autofit Inpainting Region
- If you set it on `True`, the generated image will automatically fit your inpainting region

#### Mask Blur
- With the slider, set a blur of the Inpainting Mask
	- The higher the number, the higher the blur

#### Apply Inpainting Mask
- Set on `True`, if you want to apply the Inpainting Mask to your output

***
The following settings are just for upscaling

#### Upscaler 1 and Upscaler 2
- Choose between multiple upscalers 

#### Upscaler 2 visibility
- Choose how visible the second upscaler is
    - The higher the number, the more visible is the upscaler