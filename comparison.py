#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

import torch
from torch import nn, optim
from torch.nn import functional as F
# import dataloader from torch
#import dataset
# import toTesor
import torchvision
from torchvision import transforms
from torchvision.io import read_image
from torch.utils.data import DataLoader, Dataset
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
import sys
from PIL import Image
import cv2
from torchvision.transforms import Compose, RandomCrop, ToTensor, ToPILImage, CenterCrop, Resize

from dataset import TrainDatasetFromFolder
from model import Generator, Discriminator, GeneratorLoss
from tqdm import tqdm
from torch.autograd import Variable


# In[2]:


torch.autograd.set_detect_anomaly(True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device


# In[3]:

#
# def get_factor(path):
#     return int(path.split('_')[1])
#
# factors = [get_factor(path) for path in os.listdir('models')]
# factors
#

UPSCALE_FACTOR = 32
CROP_SIZE = 128
N_EPOCHS = 5
#
#
# # # Get All Models
#
# # In[4]:
#
#
# # generators = [Generator(factors[0]).to(device) for i in range(len(os.listdir('models')))]
# generators = [Generator(factors[0]).to(device) for i in range(1)]
#
# # # Load Models
#
# # In[6]:
#
# for i, file in enumerate(os.listdir("models")):
#     generators[i].load_state_dict(torch.load(join("models", file), map_location=device))
#     generators[i].eval()
#     break
# # In[13]:
#
#
# img = Image.open("data/original/train/image_0.jpg")
# # resize the image to 96x96
# img = img.resize((96 , 24))
#
# # convert to tensor
# img = ToTensor()(img)
#
# # add batch dimension
# img = img.unsqueeze(0)
#
# img = img.to(device)
#
#
# # In[14]:
# models =  [generators[i](img) for i in range(len(generators))]
#
#
# # In[21]:
#
# plt.figure(figsize=(20, 10))
# # there are 31 subplots in the dataset
# #show low resolution image
# # plt.subplot(5, 1, 1)
# # plt.imshow(img[0].cpu().detach().permute(1, 2, 0))
# # plt.title("Low Resolution")
#
# # show models
# for i in range(len(models)):
#     # there are 5*6 subplots in the dataset
#     plt.subplot(1, len(models), i+1)
#     plt.imshow(models[i][0].cpu().detach().permute(1, 2, 0))
#     plt.title("x" + str(factors[i]))
#
#
# # save images
# plt.savefig("predicted/comparison.png")
# plt.show()


UPSCALE_FACTOR = 16
netG_nn = Generator(UPSCALE_FACTOR)
netG_nn = netG_nn.to(device)

netG_nn.load_state_dict(torch.load("good_models/linear_16_128_30.pth", map_location=device))
netG_nn.eval()

img_path = "data/original/train/image_4.jpg"
# img_path = "data/original/train/image_9.jpg"
#%%
img = Image.open(img_path)
original_image = Image.open(img_path)
print(original_image.size)

img = img.crop((0, 0, 1072, 480))
print(img.size)
# 1072, 480

target = img

# resize the image to 96x96
plt.imshow(img)
# plt.title("Original HD")
# plt.savefig("comparison_figures/fig2_hd")
plt.show()

#linx, bilinx, boxx, nnx, bicubicx, lanczos, hamming

img = img.resize((67, 30), Image.LINEAR)
print(img.size)
plt.imshow(img)
# plt.title("Box Filter Downsampled")
# plt.savefig("comparison_figures/fig2_lr_box_8")

plt.show()

# convert to tensor
img = ToTensor()(img)


# add batch dimension
img = img.unsqueeze(0)

img = img.to(device)


nearest = netG_nn(img)
nearest = nearest.squeeze(0).detach().cpu().permute(1, 2, 0)
print(nearest.shape)

predicted = nearest


# plt.imshow(nearest)
# plt.title("Super Resolution 8x Upscaled (Box)")
# plt.savefig("comparison_figures/fig2_sru_box_8")


target = np.array(target)
plt.imshow(target)
plt.show()
print(target.size, type(target))

predicted = predicted.numpy()


plt.imshow(predicted)
plt.show()
print(predicted.size, type(predicted))

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

print(f"PSNR: {psnr(target, predicted)}, SSIM: {ssim(target, predicted, multichannel=True)}")

