# default URL for connecting to the API
DEFAULT_API_URL = 'http://localhost:7860'

# layer name used for inpainting
MASK_LAYER_NAME = 'Inpainting Mask'

# options for the target
IMAGE_TARGETS = ['Layers', 'Images']

# different modes available for image processing
MODES = ['Text to Image', 'Image to Image', 'Inpainting']

# options for the fill mode in inpainting
INPAINTING_FILL_MODE = ['Fill', 'Original', 'Latent noise', 'Latent nothing']

# upscaling method options
UPSCALERS = ['None', 'Lanczos', 'Nearest', 'LDSR',
             'ESRGAN_4x', 'SwinIR_4x', 'ScuNET', 'ScuNET PSNR']

# sample method options 
SAMPLERS = [
    'Euler a', 'Euler', 'LMS', 'Heun', 'DPM2', 'DPM2 a', 'DPM++ 2S a', 'DPM++ 2M', 'DPM++ SDE', 'DPM fast',
    'DPM adaptive', 'LMS Karras', 'DPM2 Karras', 'DPM2 a Karras', 'DPM++ 2S a Karras', 'DPM++ 2M Karras',
    'DPM++ SDE Karras', 'DDIM', 'PLMS'
]

COLOR_SCHEME = {
    "primary": "#bb86fc",
    "foreground": "#ffffff",
    "on_mid": "#b3b3b3",
    "mid": "#505050",
    "background": "#2c2c2c"

}

# text that is displayed during the drawing process
PROGRESS_TEXTS = [
            "AI is drawing...",
            "Unpacking Creativity...",
            "Igniting the AI's passion for painting...",
            "Stabilizing the diffusion...",
            "Constructing the masterpiece one pixel at a time...",
            "Generating the next Van Gogh...",
            "AI is taking a coffee break...",
            "Inspiriation is flowing...",
            "AI is thinking...",
            "Adding perspective...",
            "AI is painting...",
            "Putting life into the painting...",
            "Adding a sprinkle of magic to the artwork...",
            "Adding a touch of color...",
            "Adding the Background...",
            "AI is dancing with the muse of creativity...",
            "Cleaning digital brushes...",
            "AI is getting into the flow...",
            "Adding Love...",
            "AI is doing it's best (aren't we all?)..."
        ]