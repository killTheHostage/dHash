# -*- coding : UTF-8 -*-

import cv2 as cv
from PIL import Image
import os
import numpy as np
import copy
import matplotlib.pyplot as plt

def openImg_opencv(filename = 'new.jpg'):
    if os.path.exists(filename):
        image = cv.imread(filename) #opencv
        return image
    else:
        print("image not found")

def openImg_PIL(filename = 'new.jpg'):
    if os.path.exists(filename):
        temp = Image.open(filename) #PIL
        image = np.array(temp)
        return image
    else:
        print("image not found")

def averageGray(image):
    image = image.astype(int)
    for y in range(image.shape[1]): # y is width
        for x in range(image.shape[0]): # x is height
            gray = (image[x,y,0] + image[x,y,1] + image[x,y,2]) // 3
            image[x,y] = gray
    return image.astype(np.uint8)

def averageGrayWithWeighted(image):
    image = image.astype(int)
    for y in range(image.shape[1]): # y is width
        for x in range(image.shape[0]): # x is height
            gray = image[x,y,0] * 0.3 + image[x,y,1] * 0.59 + image[x,y,2] * 0.11
            image[x,y] = int(gray)
    return image.astype(np.uint8)

def maxGray(image):
    for y in range(image.shape[1]): # y is width
        for x in range(image.shape[0]):
            gray = max(image[x,y]) # x is height
            image[x,y] = gray
    return image

def resize_opencv(image,weight = 8,height = 8):
    smallImage = cv.resize(image,(weight,height),interpolation=cv.INTER_LANCZOS4)
    return smallImage

def calculateDifference(image,weight = 8,height = 8):
    differenceBuffer = []
    for x in range(weight):
        for y in range(height - 1):
            differenceBuffer.append(image[x,y,0] > image[x,y + 1,0])
    return differenceBuffer

def makeHash(differ):
    hashOrdString = "0b"
    for value in differ:
        hashOrdString += str(int(value))
    hashString = hex(int(hashOrdString,2))
    return hashString

def stringToHash(filename = 'new.jpg'):
    image1 = openImg_opencv(filename)
    grayImage1 = averageGrayWithWeighted(copy.deepcopy(image1))
    plt.imshow(grayImage1)
    plt.show()
    smallImage1 = resize_opencv(copy.deepcopy(grayImage1))
    plt.imshow(smallImage1)
    plt.show()
    differ = calculateDifference(copy.deepcopy(smallImage1))
    return makeHash(differ)

def calculateHammingDistance(differ1,differ2):
    difference = (int(differ1, 16)) ^ (int(differ2, 16))
    return bin(difference).count("1")

def main():
    pic1 = stringToHash('3.jpg')
    pic2 = stringToHash('4.jpg')
    print("this two picture is " + str((8 * 8 - calculateHammingDistance(pic1,pic2)) / (8 * 8) * 100) + "% similarity")
if __name__ == "__main__":
    main()