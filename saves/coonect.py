import cv2
import numpy as np
import glob

frameSize = (640, 480)

out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 20, frameSize)

for filename in glob.glob('c/*.jpg'):
    print(filename)
    img = cv2.imread(filename)
    img = cv2.resize(img, (640, 480))
    out.write(img)

out.release()