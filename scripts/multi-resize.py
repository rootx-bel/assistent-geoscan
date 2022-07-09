import cv2
import numpy as np

# EDIT THIS VALUE
images=500


count=0
errors=0
while count != images:
    img = cv2.imread("%03d.jpg" % count, cv2.IMREAD_COLOR)
    try:
        new = cv2.resize(img, (640, 480))
        cv2.imwrite("%03d.jpg" % count, new)
    except:
        print("Error in {}.".format(count + 1))
        errors+=1
    else:
        print("Process {} / {}".format(count+1, images))
    count += 1
print("Done! Found errors: " + str(errors))    
