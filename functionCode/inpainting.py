import torch
import os
import twoimagelist
from torch import autocast
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline
from diffusers import AutoencoderKL
from diffusers import DPMSolverMultistepScheduler
from diffusers import StableDiffusionImg2ImgPipeline
from RealESRGAN import RealESRGAN

device = "cuda"
model_id_or_path = "runwayml/stable-diffusion-inpainting"

def in_painting(pp, np, filter, uploaded, mimage_path,user,stdname,share):
    prompt = pp #+ ", (masterpiece:1.2), best quality, ultra-detailed, illustration, portrait"
    negative_prompt = np #+ "badhandv4,(worst quality:1.6),(low quality:1.6),  easynegative"
    if filter=="PastelMix":        
        ckpt_diff = r"Stable-diffusion\pastelmix_diffuser"
        ckpt_path = r"Stable-diffusion\pastelmix-fp16.safetensors"
        vae_repo = "lint/anime_vae"
    elif filter=="Ghibli1":
        ckpt_diff = r"Stable-diffusion\ghibliJin_diffuser"
        ckpt_path = r"Stable-diffusion\ghibliStyleMix_v10.ckpt"
        vae_repo = "lint/anime_vae"
    elif filter=="CetusMix":
        ckpt_diff=r"Stable-diffusion\cetusMix_diffuser"
        ckpt_path=r"Stable-diffusion\cetusMix_Whalefall2.safetensors"
        vae_repo = "redstonehero/kl-f8-anime2"
    elif filter=="MajicMix":
        ckpt_diff=r"Stable-diffusion\majicmix_diffuser"
        ckpt_path=r"Stable-diffusion\majicmixRealistic_betterV2V25.safetensors"
        vae_repo = "lint/anime_vae"
    #-------------------high res.fix-----------------------------
    # pipe = StableDiffusionInpaintPipeline.from_pretrained(ckpt_diff,revision="fp16",torch_dtype=torch.float16,)
    # pipe.safety_checker = None
    # pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    # pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    # pipe.load_textual_inversion(r"function\badhandv4.pt")
    # pipe = pipe.to('cuda')
    # model = RealESRGAN('cuda', scale=2)
    # model.load_weights('weights/RealESRGAN_x4plus_anime_6B.pth')
    # image = Image.open(uploaded).convert("RGB")
    # init_image = image.resize((512, 512))
    # sr_image = model.predict(image)
    # sr_image = sr_image.resize((512, 512))
    # sr_image.save('up_image.png')

    # with autocast("cuda"):
    #     image = pipe(prompt=prompt,
    #                 negative_prompt=negative_prompt,
    #                 image=sr_image,
    #                 strength=0.1,
    #                 guidance_scale=11,
    #                 num_inference_steps=200,
    #                 ).images[0]
    # upscaled_image=f'static/uploaded/inpaint_{twoimagelist.Now_idx()}.jpeg'
    # image.save(upscaled_image)
    #-------------------------------------------------------------------------
    #------------------------마스크 생성----------------------------------------
    image = Image.open(uploaded).convert("RGB")
    mask_image = Image.open(mimage_path).convert("RGB")
    #-------------------------------------------------------------------------
    pipe = StableDiffusionInpaintPipeline.from_pretrained(ckpt_diff,revision="fp16",torch_dtype=torch.float16,)
    pipe.safety_checker = None
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')

    with autocast('cuda'):
        image = pipe(prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=image,
                    mask_image=mask_image,
                    guidance_scale=11,
                    num_inference_steps=100
                    ).images[0]
    image.save(f"static/in_painting/{prompt}.jpeg")

    #--------------------------------원본 이미지 필터 적용-----------------------------------
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    pipe = StableDiffusionImg2ImgPipeline.from_ckpt(ckpt_path, num_hidden_layers=11, torch_dtype=torch.float16)
    pipe.safety_checker = None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to(device)

    image_path = f"static/in_painting/{prompt}.jpeg"

    image = Image.open(image_path).convert("RGB")
    init_image = image.resize((512, 512))

    generator = torch.Generator(device="cuda").manual_seed(-1)

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=init_image,
                    strength=0.1,
                    guidance_scale=11,
                    num_inference_steps=100
                    ).images[0]
    images.save(f"static/in_painting/{prompt}.jpeg")
    #----------------------------------------------------------------------------------------
    #-------------------high res.fix-----------------------------

    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4plus_anime_6B.pth')
    sr_image = model.predict(images)
    sr_image = sr_image.resize((512, 512))
    sr_image.save('up_image.png')

    with autocast("cuda"):
        image = pipe(prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=sr_image,
                    strength=0.1,
                    guidance_scale=11,
                    num_inference_steps=200,
                    ).images[0]
    os.remove(f"static/in_painting/{prompt}.jpeg")
    result_image=f"static/in_painting/inpaint_{twoimagelist.Now_idx()}.jpeg"
    image.save(result_image)
    twoimagelist.save(twoimagelist.Now_idx(),user,stdname, prompt, negative_prompt,filter, uploaded, mimage_path, result_image, share)
    #-------------------------------------------------------------------------