import cv2
import numpy as np

cap = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1280, 960))
dim = (1280, 960)
while True:
    
    ret, frame = cap.read()
    frame = cv2.resize(frame, dim)
    out.write(frame)
    
    cv2.imshow('CAM', frame)   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
