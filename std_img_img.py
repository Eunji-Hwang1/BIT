import torch
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image
import base64
from io import BytesIO

def img_to_img(image_prompt, image_data):
    torch.backends.cuda.max_split_size_mb = 1024  # 예: 1024 MB로 설정
    device = "cuda"
    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)
    print(image_data)
    image_bytes = base64.b64decode(image_data.split(",")[1])
    image = Image.open(BytesIO(image_bytes)) 
    init_image = image.resize((100,100))

    image = pipe(prompt=image_prompt, image=init_image, strength=0.75, guidance_scale=7.5, num_inference_steps=30).images[0]
    image.save("static/testimg/"+image_prompt+".jpeg")
    
    