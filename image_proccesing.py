import cv2
import asyncio
from PIL import Image
import numpy as np
import pytesseract
from math import sqrt



def is_givaway(img, basevalue, dislimit):
    mean = cv2.mean(img)
    distance = sqrt(((mean[0]-basevalue[0])**2) + ((mean[0]-basevalue[0])**2) + ((mean[2]-basevalue[2])**2))
    return distance < dislimit

def get_text(img):
    img[:, :, 2] = 0
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    width = int(img.shape[1] * 90 / 100)
    height = int(img.shape[0] * 90 / 100) 
    dim = (width, height) 
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    img = cv2.fastNlMeansDenoising(img)
    return pytesseract.image_to_string(img, lang="engpirate+eng")

if __name__ == '__main__':
    img = cv2.imread("sample4.png")
    if is_givaway(img, (6.407418514812385, 5.406766752083711, 63.57950020636679), 1):
        print(get_text(img))