import cv2

import cv2
# create the estimator! tbm
def showzone():
    global img
    overlay = img.copy()
    cv2.ellipse(overlay, (150, 400),(33,60), 0,0,360, (0, 255, 0), -1)
    alpha = 0.4  # Transparency factor.
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

# click event function from stackoverflow;
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
        cv2.circle(img, (x, y), 9, (0, 0, 0), -1)
        cv2.circle(img, (x,y), 8, (0,0,255), -1)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.circle(img, (x, y), 9, (0, 0, 0), -1)
        cv2.circle(img, (x, y), 8, (0, 192, 255), -1)


img = cv2.imread('baseplate.jpg', 1)
cv2.namedWindow('nextshotcurl')
cv2.setMouseCallback('nextshotcurl', click_event)
while(1):
    cv2.imshow('nextshotcurl', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 13:
        print('yo!')
        showzone()
    if k == 27:
        break
cv2.destroyAllWindows()
