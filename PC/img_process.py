import urllib.request
import cv2
import numpy as np


IMG_WIDTH = 100
IMG_HEIGH = 50



def get_processed_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi = img[100:,0:]
    guass = cv2.GaussianBlur(roi,(5,5),0)
    ret, roi_bin= cv2.threshold(guass, 170, 255, cv2.THRESH_BINARY)
    roiResize = cv2.resize(roi_bin, (IMG_WIDTH,IMG_HEIGH ))
    return roi_bin, roiResize

def get_image_url(url):
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    return img


