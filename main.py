import cv2
import os
import itertools
import numpy as np
import pandas as pd
import imutils

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)

#heart = cv2.imread(r'w2.png', cv2.IMREAD_GRAYSCALE)
#_, mask = cv2.threshold(heart, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

folder_to_view = 'images'
mask_folder = 'masks'
for i, file in enumerate(os.listdir(folder_to_view)):
    throw_dict = {'g1':0,'g2':0,'g3':0,'g4':0,
    'e1':0,'e2':0,'e3':0,'e4':0,'e5':0,'e6':0,
    'w1':0,'w2':0,'w3':0,'w4':0,'w5':0,'w6':0,
    'i1':0,'i2':0,'i3':0,'i4':0,'i5':0,'i6':0,'i7':0,'i8':0,
    'bl':0,'br':0,
    'c':0}
    print(os.listdir(folder_to_view))
    print(os.listdir(mask_folder))
    row_list = []
    img = cv2.imread(folder_to_view+'/' + file)
    for j,maskfile in enumerate(os.listdir(mask_folder)):
        print(maskfile)
        print(maskfile.replace('.png',''))
        zone = cv2.imread(mask_folder + '/' + maskfile, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(zone, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
        masked = cv2.bitwise_and(img, img, mask=mask)
        red_bin = cv2.inRange(masked, (0, 0, 255), (0, 0, 255))
        yellow_bin = cv2.inRange(masked, (0, 192, 255), (0, 255, 255))
        blue_bin = cv2.inRange(masked, (255, 0, 0), (255, 63, 0))
        greyish_yellow_bin = cv2.inRange(masked, (0, 164, 207), (32, 224, 239))
        yellow_rocks = cv2.bitwise_or(yellow_bin, cv2.bitwise_or(blue_bin,
                                                                 greyish_yellow_bin))
        # detect the contors WITHOUT looking at the mask
        if np.any(yellow_rocks != 0):
            print(maskfile.replace('.png', '') + 'in the ' + file)
            # throw_dict[maskfile.replace('.png','')] += 1
            ret, thresh = cv2.threshold(yellow_rocks, 200, 255, 0)
            contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            #only_rocks = np.array(contours)
            cv2.drawContours(masked, contours, -1, (0, 255, 0), 1)
            for cnt in contours:
                M = cv2.moments(cnt)
                cx = M['m10'] / max(M['m00'], 1)
                cy = M['m01'] / max(M['m00'], 1)
                print(cx)
                print(cy)
            for x in contours:
                throw_dict[maskfile.replace('.png', '')] += 1
            cv2.imshow('roi', masked)
            cv2.waitKey(0)
            # print('done')
            cv2.destroyAllWindows()
        # INCREASE COUNTER FOR EVERY RED STONE IN ZONE!
        if np.any(red_bin != 0):
            print(maskfile.replace('.png','') + 'in the ' + file)
            #throw_dict[maskfile.replace('.png','')] += 1
            ret, thresh = cv2.threshold(red_bin, 127, 255, 0)
            contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(masked, contours, -1, (0, 255, 0), 1)

            for x in contours:
                throw_dict[maskfile.replace('.png', '')] += 1


            cv2.imshow('roi', masked)
            cv2.waitKey(0)
            #print('done')
            cv2.destroyAllWindows()
    print(throw_dict)
    print(True in row_list)

# cv2.setMouseCallback('image', click_event)



