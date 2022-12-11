import unreal_engine as ue
from unreal_engine.enums import EPixelFormat

import time

# 确保已使用`huggingface-cli login`登录huggingface
from torch import autocast
from diffusers import StableDiffusionPipeline

class RuntimeImage:

    def begin_play(self):
        width = 512
        height = 512
        self.texture = ue.create_transient_texture(width, height, EPixelFormat.PF_R8G8B8A8)

        self.uobject.get_owner().Plane.OverrideMaterials[0].set_material_texture_parameter('Texture', self.texture)

        self.uobject.get_owner().bind_event('GenerateTexture', self.generate_texture)
    
    def generate_texture(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4", 
            use_auth_token=True
        ).to("cuda")

        prompt = "girl"
        with autocast("cuda"):
            image = pipe(prompt).images[0]
        
        image_path = ue.get_game_saved_dir() + "Autosaves/{0}_{1}.png".format(prompt,time.time())
        image.save(image_path)

        image_bytes = image.tobytes("raw", "RGBA")
        print(len(image_bytes))

        self.texture.texture_set_data(image_bytes)

