import cv2
import pandas as pd
from joblib import load
import cv2
from guimask import bigfunc
# This is a modified masking function, not from test_main module
from cleanup import cleanup
# load in the models for x cords and y-cords
xmod = load('xmodel.joblib')
ymod = load('ymodel.joblib')

def showzone():
    global img
    overlay = img.copy()
    playingfield = bigfunc(img) # using the computer vision function we created to get the stone locations.
    playingfieldpd = pd.DataFrame([playingfield])
    playingfield_cleaned = cleanup(playingfieldpd) # since we create theses features for the model, so must these be created.
    xcord = xmod.predict(playingfield_cleaned)
    print(xcord)
    print(type(xcord))
    xcord = xcord.astype('int')
    ycord = ymod.predict(playingfield_cleaned)
    print(ycord)
    print(type(ycord))
    ycord = ycord.astype('int')
    cv2.ellipse(overlay, (xcord[0], ycord[0]),(33,60), 0,0,360, (0, 255, 0), -1)
    alpha = 0.4  # Transparency factor.
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)


def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        # Red Stones
        cv2.circle(img, (x, y), 9, (0, 0, 0), -1)
        cv2.circle(img, (x,y), 8, (0,0,255), -1)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        # Yellow stones
        cv2.circle(img, (x, y), 9, (0, 0, 0), -1)
        cv2.circle(img, (x, y), 8, (0, 192, 255), -1)


img = cv2.imread('baseplate.jpg', 1)
cv2.namedWindow('nextshotcurl')
cv2.setMouseCallback('nextshotcurl', click_event)
while(1):
    cv2.imshow('nextshotcurl', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 13:
        print('Showing Results')
        showzone()
    if k == 27: # esc key
        break
cv2.destroyAllWindows()
