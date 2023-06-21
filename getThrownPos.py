import cv2
import os
import itertools
import numpy as np
import pandas as pd
import imutils

def getThrownCord(imgp):
    cx = 0;
    cy = 0;
    reta, thresha = cv2.threshold(imgp, 0, 10, 0)
    contoursa, hierachya = cv2.findContours(thresha, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    for contour in contoursa:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 1) & (area > 20) & (area < 150)):
            contour_list.append(contour)
            M = cv2.moments(contour)

            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                print('recognized at' + str(cx) + ' ' + str(cy))
                cv2.imshow('roi', imgp)
                cv2.waitKey(0)
                cv2.drawContours(imgp, contour, -1, (0, 255, 0), 5)
                break;
    sol = []
    sol.append(cx)
    sol.append(cy)
    return sol
