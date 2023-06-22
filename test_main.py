import cv2
import os
import itertools
import numpy as np
import pandas as pd
import imutils
from getThrownPos import getThrownCord
folder_to_view = 'images'
mask_folder = 'tostore'

def bigfunc(file, toflip):
#for i, file in enumerate(os.listdir(folder_to_view)):
    throw_dict = {'g1':0,'g2':0,'g3':0,'g4':0,'g5':0,'g6':0,'g7':0,'g8':0,'g9':0,'g10':0,'g11':0,'g12':0,'g13':0,'g14':0,'g15':0,'g16':0,
    'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'h7': 0, 'h8': 0,
    'ei1': 0, 'ei2': 0, 'ei3': 0, 'ei4': 0, 'ei5': 0, 'ei6': 0, 'ei7': 0, 'ei8': 0, 'ei9': 0, 'ei10': 0,'ei11': 0, 'ei12': 0, 'ei13': 0, 'ei14': 0, 'ei15': 0, 'ei16': 0,
    'eo1': 0, 'eo2': 0, 'eo3': 0, 'eo4': 0, 'eo5': 0, 'eo6': 0, 'eo7': 0, 'eo8': 0, 'eo9': 0, 'eo10': 0,'eo11': 0, 'eo12': 0, 'eo13': 0, 'eo14': 0, 'eo15': 0, 'eo16': 0,

    'wi1':0,'wi2':0,'wi3':0,'wi4':0,'wi5':0,'wi6':0,'wi7':0,'wi8':0,'wi9':0,'wi10':0,'wi11':0,'wi12':0,'wi13':0,'wi14':0,'wi15':0,'wi16':0,
    'wo1': 0, 'wo2': 0, 'wo3': 0, 'wo4': 0, 'wo5': 0, 'wo6': 0, 'wo7': 0, 'wo8': 0, 'wo9': 0, 'wo10': 0, 'wo11': 0,'wo12': 0, 'wo13': 0, 'wo14': 0, 'wo15': 0, 'wo16': 0,
    'i1':0,'i2':0,'i3':0,'i4':0,'i5':0,'i6':0,'i7':0,'i8':0,'i9':0,'i10':0,'i11':0,'i12':0,'i13':0,'i14':0,'i15':0,'i16':0,
    'bl':0,'br':0,
    'c':0}
    #print(os.listdir(mask_folder))
    row_list = []
    img = cv2.imread(file)
    imgp = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if (toflip == True):
        img = cv2.rotate(img, cv2.ROTATE_180)
        imgp = cv2.rotate(imgp, cv2.ROTATE_180)
    #cv2.imshow('roi', img)
    #cv2.imshow('roi', imgp)
    #cv2.waitKey(0)
    xylist = getThrownCord(imgp)
    throw_dict['thrownx'] = xylist[0] #x
    throw_dict['throwny'] = xylist[1] #y

    confirmed_x = []
    confirmed_y = []
    circles = cv2.HoughCircles(imgp, cv2.HOUGH_GRADIENT, 1, 6,
                            param1 = 250 ,param2 = 20, minRadius = 6, maxRadius = 10)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            #print(x)
            #print(y)
            for extra in range(0,10):
                confirmed_x.append(x+extra)
                confirmed_y.append(y+extra)
                confirmed_x.append(x - extra)
                confirmed_y.append(y - extra)

    #print(confirmed_x)
    #print(confirmed_y)
    #cv2.imshow('cimg', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    for j,maskfile in enumerate(os.listdir(mask_folder)):
        #print(maskfile.replace('.png',''))
        zone = cv2.imread(mask_folder + '/' + maskfile, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(zone, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
        masked = cv2.bitwise_and(img, img, mask=mask)
        red_bin = cv2.inRange(masked, (0, 0, 255), (0, 0, 255))
        yellow_bin = cv2.inRange(masked, (0, 192, 255), (0, 255, 255))
        blue_bin = cv2.inRange(masked, (255, 0, 0), (255, 63, 0))
        greyish_yellow_bin = cv2.inRange(masked, (0, 164, 207), (32, 224, 239))
        yellow_rocks = cv2.bitwise_or(yellow_bin, cv2.bitwise_or(blue_bin, greyish_yellow_bin))
        # DETERMINE THE "THROWN STONE"

        # INCREASE COUNTER FOR EVERY YELLOW STONE
        if np.any(yellow_rocks != 0):
            #print(maskfile.replace('.png', '') + 'in the ' + file)
            # throw_dict[maskfile.replace('.png','')] += 1
            ret, thresh = cv2.threshold(yellow_rocks, 200, 255, 0)
            contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            #only_rocks = np.array(contours)
            cv2.drawContours(masked, contours, -1, (0, 255, 0), 1)
            #for cnt in contours:
            #    M = cv2.moments(cnt)
            #    cx = M['m10'] / max(M['m00'], 1)
            #    cy = M['m01'] / max(M['m00'], 1)
            #    print(cx)
            #    print(cy)
            for x in contours:
                M = cv2.moments(x)
                cx = M['m10'] / max(M['m00'], 1)
                cy = M['m01'] / max(M['m00'], 1)
                #print(cx)
                #print(cy)
                if (abs(cx-xylist[0]) < 4) and (abs(cy-xylist[1]) < 4):
                    pass
                    #print('too close to recognized stone; don\'t include')
                else:
                    if int(cx) in confirmed_x and int(cy) in confirmed_y:
                        #print('ok!')
                        throw_dict[maskfile.replace('.jpg', '')] += 1
                    else:
                        pass
                        #print('probable ghost stone')
            #cv2.imshow('roi', masked)
            #cv2.waitKey(0)
            # print('done')
            #cv2.destroyAllWindows()
        # INCREASE COUNTER FOR EVERY RED STONE IN ZONE!
        if np.any(red_bin != 0):
            #print(maskfile.replace('.png','') + 'in the ' + file)
            #throw_dict[maskfile.replace('.png','')] += 1
            ret, thresh = cv2.threshold(red_bin, 127, 255, 0)
            contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(masked, contours, -1, (0, 255, 0), 1)

            for x in contours:
                #print('doing things')
                M = cv2.moments(x)
                cx = M['m10'] / max(M['m00'], 1)
                cy = M['m01'] / max(M['m00'], 1)
                if (abs(cx - xylist[0]) < 4) and (abs(cy - xylist[1]) < 4):
                    pass
                    #print('too close to recognized stone; don\'t include')
                else:
                    if int(cx) in confirmed_x and int(cy) in confirmed_y:
                        #print('ok!')
                        throw_dict[maskfile.replace('.jpg', '')] += 1
                    else:
                        pass
                        #print('probable ghost stone')

            #cv2.imshow('roi', masked)
            #cv2.waitKey(0)
            #print('done')
            #cv2.destroyAllWindows()
    #print(throw_dict)
    #print(True in row_list)
    return throw_dict
# cv2.setMouseCallback('image', click_event)
