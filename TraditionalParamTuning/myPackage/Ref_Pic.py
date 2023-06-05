import cv2
import os

def gen_ref_denoise(N):
    
    for i, f in enumerate(os.listdir('Ref_Pic/capture')):
        print(f)
        if i==0:
            img = cv2.imread('Ref_Pic/capture/'+f)/255
        else:
            img += cv2.imread('Ref_Pic/capture/'+f)/255
        if i+1 == N: break

    img /= N
    cv2.imwrite('Ref_Pic/ref_denoise_{}.jpg'.format(N), (img*255).astype(int))

import kornia
import cv2
import numpy as np
import torch
from torchvision.utils import save_image

def gen_ref_sharpness(N):
    img: np.ndarray = cv2.imread('Ref_Pic/ref_denoise_{}.jpg'.format(N))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    data: torch.tensor = kornia.utils.image_to_tensor(img, keepdim=False)
    data = data.float() / 255

    # kornia.filters.UnsharpMask(kernel_size, sigma) kernel_size越大，白邊越強
    sharpen = kornia.filters.UnsharpMask((7,7), (2.5,2.5))
    sharpened_tensor = sharpen(data)
    # difference = (sharpened_tensor - data).abs()
    save_image(sharpened_tensor, 'Ref_Pic/ref_sharpened_{}.jpg'.format(N))



