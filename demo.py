#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from models.blip import blip_decoder

# 检查是否提供了输入和输出文件路径
if len(sys.argv) != 3:
    print("Usage: python script.py <input_image_path> <output_caption_path>")
    sys.exit(1)

input_image_path = "../uploads/image_test.png"
output_caption_path = "../output_temp.txt"

# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_demo_image(image_size, device, img_path):
    raw_image = Image.open(img_path).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((image_size, image_size), interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ])
    image = transform(raw_image).unsqueeze(0).to(device)
    return image

image_size = 384
image = load_demo_image(image_size=image_size, device=device, img_path=input_image_path)

# 加载模型权重
model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'
model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)

with torch.no_grad():
    # 使用 nucleus sampling 生成描述
    caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5)
    print('Caption: ' + caption[0])

# 将生成的描述写入到文件
with open(output_caption_path, 'w', encoding='utf-8') as f:
    f.write(caption[0])

print(f"Caption has been written to {output_caption_path}")
