# Video to Photos(1280x960)
import cv2
count=0
frame=6
video= cv2.VideoCapture("c.mp4")
success, image = video.read()
while success:
    success,image = video.read()
    if frame==6:
        resize = cv2.resize(image, (1280, 960)) 
        cv2.imwrite("%03d.jpg" % count, resize)
        count+=1
        frame=0
    else:
        frame+=1
