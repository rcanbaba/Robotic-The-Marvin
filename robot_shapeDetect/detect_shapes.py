#BELOW CODE TAKEN FROM
# https://stackoverflow.com/questions/49792226/opencv-python-shape-detection
# I made some necessary corrections following video tutorial FROM:
# https://pysource.com/2018/09/25/simple-shape-detection-opencv-with-python-3/

import cv2
#from shapedetector import ShapeDetector

COUNT = 0
class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = ""
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        #print("value of approx", approx)

        if len(approx) == 3:
            shape = "Triangle"
            #print("Triangle")

        elif len(approx) == 4:
            global COUNT
            COUNT = COUNT +1
            #print("value of approx", approx)
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            #print("4 kenarlı")

            #print("value of ar",ar)
            if COUNT == 2:
                if (ar >= 0.95 and ar <= 1.05): shape = "Square"
                elif (ar <= 5 and ar >= 3): shape = "Obround"
                else: shape = "Rectangle"

        elif len(approx) == 5:
            shape = "Pentagon"
            #print("Pentagon")
        elif len(approx) == 2:
            shape = "Line"
            #print("Line")
            #print("value of approx", approx)
        else:
            shape = "Circle"
            #print("Circle")
            #print("value of approx", approx)

        return shape

# JPG
image = cv2.imread('can6.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 1, 180, cv2.THRESH_BINARY)[1]
#adjust a threshold for our images..,
ksize = 5

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize,ksize))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# ~ cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = cnts[1]
sd = ShapeDetector()
for c in cnts:
    M = cv2.moments(c)
    if M["m00"] != 0:  # prevent divide by zero
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = sd.detect(c)
        print(shape)

    c = c.astype("float")
    #c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 0, 0), 2)

cv2.imshow("Image", image)
#cv2.waitKey(0)
