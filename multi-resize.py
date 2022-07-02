import cv2
import numpy as np

count=0

while count != 300:
    img = cv2.imread("%03d.jpg" % count, cv2.IMREAD_COLOR)
    try:
        new = cv2.resize(img, (640, 480))
        cv2.imwrite("%03d.jpg" % count, new)
    except:
        print("Error in {}.".format(count + 1))
    else:
        print("Process {} / 150".format(count+1))
    count += 1
    