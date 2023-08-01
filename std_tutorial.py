import os
import torch
from torch import autocast
from RealESRGAN import RealESRGAN
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
from diffusers import AutoencoderKL
import stdlist as stdlist


SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'STD', 'static', 'img')
def stdv1_5(pprompt, nprompt, filter):
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    def uniquify(path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + ' (' + str(counter) + ') ' + extension
            counter += 1

        return path

    prompt = pprompt
    negative_prompt = nprompt

    print(f"Characters in prompt: {len(prompt)}, limit: 200")
    model_id = "runwayml/stable-diffusion-v1-5"
    ckpt_path = r"Stable-diffusion\pastelmix-fp16.safetensors"
    vae_repo = "lint/anime_vae"
    #lora_path = r"C:\Users\user\Desktop\STD\function\FilmVelvia2.safetensors"
    #vae_path = r"C:\Users\user\Desktop\STD\VAE\pastel-waifu-diffusion.vae.pt"
    #pipe =CLIPTextModel.from_pretrained(model_id, subfolder="text_encoder", num_hidden_layers=11, torch_dtype=torch.float16)
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = StableDiffusionPipeline.from_ckpt(ckpt_path, torch_dtype=torch.float16, num_hidden_layers=11)
    pipe.safety_checker=None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.load_textual_inversion(r"C:\Users\user\Desktop\STD\function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"C:\Users\user\Desktop\STD\function\badhandv4.pt")
    pipe = pipe.to('cuda')
    #pipe.load_lora_weights(lora_path)

    generator = torch.Generator(device="cuda").manual_seed(-1)

    with autocast('cuda'):
        image = pipe(prompt=prompt,
                    negative_prompt=negative_prompt,
                    guidance_scale=7,  #cfg 스케일
                    num_inference_steps=30, 
                    ).images[0]
    #image_path = uniquify(os.path.join(SAVE_PATH, (prompt[:25] + '...')if len(prompt) > 25 else prompt) + '.png')
    #image.save("static/unupscale/"+prompt+"_.jpeg")
    
    
    # -------------------high res.fix-----------------------------
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = StableDiffusionImg2ImgPipeline.from_ckpt(ckpt_path, torch_dtype=torch.float16, num_hidden_layers=11)
    pipe.safety_checker=None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.load_textual_inversion(r"C:\Users\user\Desktop\STD\function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"C:\Users\user\Desktop\STD\function\badhandv4.pt")
    pipe = pipe.to('cuda')
    
    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4.pth')
    sr_image = model.predict(image)
    sr_image = sr_image.resize((512, 512))
    sr_image.save('up_image.png')

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=sr_image,
                    strength=0.5,
                    num_inference_steps=30,
                    ).images[0]
        #image_path = uniquify(os.path.join(SAVE_PATH, (prompt[:25] + '...')if len(prompt) > 25 else prompt) + '.png')
    images.save("static/testimg/"+prompt+".jpeg")
    #-------------------------------------------------------------------------
