# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np

img1 = cv2.imread('sheet0.jpg')
gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

ret, bw = cv2.threshold(gray,170,255,cv2.THRESH_BINARY)

cv2.imshow('img',bw)
cv2.waitKey(0)
cv2.destroyAllWindows()