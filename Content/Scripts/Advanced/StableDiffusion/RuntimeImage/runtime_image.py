import unreal_engine as ue
from unreal_engine.enums import EPixelFormat

import time
from PIL import Image

import time
import torch

# 确保已使用`huggingface-cli login`登录huggingface
from torch import autocast
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

class RuntimeImage:

    def begin_play(self):

        self.width = 512
        self.height = 512

        self.texture = ue.create_transient_texture(self.width, self.height, EPixelFormat.PF_R8G8B8A8)

        self.uobject.get_owner().Plane.OverrideMaterials[0].set_material_texture_parameter('Texture', self.texture)

        self.uobject.get_owner().bind_event('GenerateTexture', self.generate_texture)
    
    def generate_texture(self):

        model_name = "CompVis/stable-diffusion-v1-4"
        prompt = "beatiful scene, a European-style street with street trees, stools and small shops along the street"

        if self.uobject.get_owner().ClassName == 'text2img':

            pipe = StableDiffusionPipeline.from_pretrained(
                model_name, 
                use_auth_token=True
            ).to("cuda")

            with autocast("cuda"):
                image = pipe(prompt).images[0]
            
            image_path = ue.get_game_saved_dir() + "Autosaves/{0}_{1}.png".format(prompt,time.time())
            image.save(image_path)

            image_bytes = image.tobytes("raw", "RGBA")

            self.texture.texture_set_data(image_bytes)
        
        elif self.uobject.get_owner().ClassName == 'screen2img':
            width, height = ue.editor_get_pie_viewport_size()
            pixels = ue.editor_get_pie_viewport_screenshot()

            ue.log("{0} {1} {2}".format(width, height, len(pixels)))

            pixels_array = []

            for y in range(0, height):
                for x in range(0, width):
                    index = y * width + x
                    pixel = pixels[index]
                    pixels_array.append((pixel.r, pixel.g, pixel.b, 255))

            init_image = Image.new('RGBA', (width, height))
            init_image.putdata(pixels_array)

            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_name, 
                revision="fp16", 
                torch_dtype=torch.float16,
            ).to("cuda")
            pipe.safety_checker = lambda images, clip_input: (images, False)

            init_image = init_image.convert("RGB").resize((self.width, self.height))

            images = pipe(prompt=prompt, init_image=init_image, strength=0.75, guidance_scale=7.5).images

            image_path = ue.get_game_saved_dir() + "Autosaves/{0}_{1}.png".format(prompt,time.time())
            images[0].save(image_path)

            image_bytes = images[0].tobytes("raw", "RGBA")
            self.texture.texture_set_data(image_bytes)

