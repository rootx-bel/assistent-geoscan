import cv2

count=0
frame=6
shot=0


video= cv2.VideoCapture("vid.mp4")
success, image = video.read()

while success:
    success,image = video.read()

    if frame==30:
        resize = cv2.resize(image, (1280, 960)) 
        cv2.imwrite("%03d.jpg" % count, resize)
        count+=1
        frame=0
        shot+=1
        print("SHOT! > " + str(shot))
        
    else:
        frame+=1
                                
if count != 0: print("Done! Photo value -> " + str(shot))
else: print("Error! File not found!")

