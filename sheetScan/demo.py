# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 19:43:05 2018

@author: Rushabh
"""

import cv2
import math
import numpy as np


def front(img):
    
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret, bw = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)

    height, width = bw.shape[:2]

    #print(width, height)

    h1 = int(0.30*float(height))
    h2 = int(0.80*float(height))
    
    wtemp = int(0.2*float(width))
    
    #print(h1,h2,wtemp)
    
    roi = bw[h1:h2,0:wtemp]
    
    xs = []
    ys = []
    
    for y in range(h2-h1):
        for x in range(wtemp):
            if(roi[y,x]==0):
                break
        ys.append(y)
        xs.append(x)
    
    ysum = 0
    xsum = 0
    
    for k in range(len(ys)-2):
        ysum = ysum+(ys[k+1]-ys[k])
        xsum = xsum+(xs[k+1]-xs[k])
    
    slope = ysum/xsum
    
    #print(slope)
    
    angle = math.atan(slope)
    angle = angle*(180/math.pi)
    if(slope<0):
        angle = 90+angle
    else:
        angle = angle-90
    
    #print('Angle: ',angle)
    
    M = cv2.getRotationMatrix2D((width/2,height/2),angle,1)
    dst = cv2.warpAffine(img,M,(width,height))            
    
    dst = dst[40:height-40,40:width-40]
    dgray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
    ret, rot = cv2.threshold(dgray,200,255,cv2.THRESH_BINARY)
    
    #cv2.imwrite('border.jpeg', dst )
    
    height, width = rot.shape[:2]
    
    h1 = int(0.30*float(height))
    h2 = int(0.80*float(height))
    
    wtemp = int(0.2*float(width))
    
    w1 = int(0.3*width)
    w2 = int(0.7*width)
    
    htemp = int(0.8*height)
    
    leftreg = rot[h1:h2,0:wtemp]
    botreg = rot[htemp:height, w1:w2]
    
    lsum = 0
    lcount = 0
    
    for y in range(h2-h1):
        for x in range(wtemp):
            if(leftreg[y,x]==0):
                break
        lsum = lsum+x
        lcount += 1
        left = int(lsum/lcount)
    
    bsum = 0
    bcount = 0
    
    hreg = height-htemp-1
    
    for x in range(w2-w1):
        for y in range(hreg,0,-1):
            if(botreg[y,x]==0):
                break
        bsum = bsum+y
        bcount += 1
        bottom = height - (hreg - int(bsum/bcount))
    
    final = dst[0:bottom, left:width]
    fingray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(fingray,200,255,cv2.THRESH_BINARY) 
    
    cv2.imwrite('final.jpg', final )
    
    box = dst[600:740, 1134:1354]
    bpc = (140*220) - np.count_nonzero(box)
    #print str(bpc)+'/'+str(140*220)
    #dst[600:740, 1134:1354] = 0
    
    ht, wt = dst.shape[:2]
    
    ybdec = 9+50
    ydec = 50
    ystart = ht-5-50
    
    xbinc = 13+250
    xinc = 250
    
    res = 250*50
    starr = []
    
    for y in range(35):
        count = 0
        xstart = 982 
        yend = ystart+ydec
        for x in range(3):
            xend = xstart+xinc
            box = dst[ystart:yend, xstart:xend]
            bpc = res - np.count_nonzero(box)
            #dst[ystart:yend, xstart:xend] = 0
            #print(ystart,yend,xstart,xend,bpc)
            if(bpc>1700):
                count += 1
                dst[ystart:yend, xstart:xend] = 0
            xstart += xbinc
        starr.append(count)
        ystart -= ybdec
        
    cv2.imwrite('dst.jpeg',dst)
    totalLec = 0
    xstart = 1134
    resLec = 140*220
    for x in range(3):
        box = dst[600:740, xstart:xstart+xinc]
        if((resLec - np.count_nonzero(box)) > 5000):
            totalLec+=1
        xstart += xbinc
        
    starr.append(totalLec)
    starr.reverse()
    #print(starr)
    return starr    
    #cv2.imwrite('test1.jpg', dst)    
    
def back(img, students):
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    ret, bw = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    
    height, width = bw.shape[:2]
    
    #print(width, height)
    
    h1 = int(0.30*float(height))
    h2 = int(0.80*float(height))
    
    wtemp = int(0.2*float(width))
    
    #print(h1,h2,wtemp)
    
    roi = bw[h1:h2,0:wtemp]
    
    xs = []
    ys = []
    
    for y in range(h2-h1):
        for x in range(wtemp):
            if(roi[y,x]==0):
                break
        ys.append(y)
        xs.append(x)
    
    ysum = 0
    xsum = 0
    
    for k in range(len(ys)-2):
        ysum = ysum+(ys[k+1]-ys[k])
        xsum = xsum+(xs[k+1]-xs[k])

    xsum = xsum+0.0001
    slope = ysum/xsum
    
    #print(slope)
    
    angle = math.atan(slope)
    angle = angle*(180/math.pi)
    if(slope<0):
        angle = 90+angle
    else:
        angle = angle-90
    
    #print('Angle: ',angle)
    
    M = cv2.getRotationMatrix2D((width/2,height/2),angle,1)
    dst = cv2.warpAffine(img,M,(width,height))            
    
    dst = dst[40:height-40,40:width-40]
    dgray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
    ret, rot = cv2.threshold(dgray,200,255,cv2.THRESH_BINARY)
    
    #cv2.imwrite('borderback.jpeg', dst )
    
    height, width = rot.shape[:2]
    
    h1 = int(0.30*float(height))
    h2 = int(0.80*float(height))
    
    wtemp = int(0.2*float(width))
    
    w1 = int(0.3*width)
    w2 = int(0.7*width)
    
    htemp = int(0.2*height)
    
    leftreg = rot[h1:h2,0:wtemp]
    botreg = rot[0:htemp, w1:w2]
    
    lsum = 0
    lcount = 0
    
    for y in range(h2-h1):
        for x in range(wtemp):
            if(leftreg[y,x]==0):
                break
        lsum = lsum+x
        lcount += 1
        left = int(lsum/lcount)
    
    bsum = 0
    bcount = 0
    
    #hreg = htemp
    
    for x in range(w2-w1):
        for y in range(htemp):
            if(botreg[y,x]==0):
                break
        bsum = bsum+y
        bcount += 1
        bottom = int(bsum/bcount)
    
    final = dst[bottom:height, left:width]
    fingray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(fingray,200,255,cv2.THRESH_BINARY) 
    
    cv2.imwrite('finalback.jpg', final )
    
    box = dst[2515:2643,2695:3145]
    
    count = 0
    boxarr = np.asarray(box)
    count = np.count_nonzero(box)
    count = 128*450-count
    #print(count)
    
    '''
    ystart 5980
    yend 6090
    ybuff 26
    ydec = 110
    
    xstart 2230
    xend 2670
    xbuff 30
    xinc 440
    '''
    
    ht, wt = dst.shape[:2]
    
    ybdec = 9+50
    ydec = 50
    ystart = 65
    
    xbinc = 13+250
    xinc = 250
    
    res = 250*50
    starr = [0]
    
    for y in range(students):
        count = 0
        xstart = 966 
        yend = ystart+ydec
        for x in range(3):
            xend = xstart+xinc
            box = dst[ystart:yend, xstart:xend]
            bpc = res - np.count_nonzero(box)
            #dst[ystart:yend, xstart:xend] = 0
            #print(ystart,yend,xstart,xend,bpc)
            if(bpc>1700):
                count += 1
                dst[ystart:yend, xstart:xend] = 0
            xstart += xbinc
        starr.append(count)
        ystart += ybdec

    cv2.imwrite('dstb.jpeg', dst)    
    return starr
