from importlib.util import find_spec

import cv2
import os
import numpy as np
from pyparsing import original_text_for

roi_points = []
()
def make_black(frame):
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    mask_inv = cv2.bitwise_not(mask)
    blacked_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
    return blacked_frame



VIDEO_PATH = 'Rallies/Rally2.mp4'
OUTPUT_DIR = 'Outputs'
MIN_AREA=5000
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame1 = cap.read()
ret, frame2 = cap.read()
temp = frame1.copy()

frame_count=0
def mousecallback(event,x,y,flags,parameter):
    global roi_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(roi_points)<4:
            roi_points.append((x,y))
            print(f"# of points = {len(roi_points)}")

finishedMousecallback = False
cv2.namedWindow("select roi")
cv2.setMouseCallback("select roi",mousecallback)
while True:
    display=temp.copy()
    for points in roi_points:
        cv2.circle(display,np.array(roi_points),False,(0,0,0),2)
    if len(roi_points)==4:
        cv2.polylines(display,np.array(roi_points),True,(0,0,0),2)
        cv2.imshow("select roi",display)
        cv2.waitKey(500)
        finishedMousecallback=True
        break
    if cv2.waitKey(30) & 0xFF == 27:  # esc to exit
        break


#frame differencing
while ret and finishedMousecallback:
    shuttle_contours = []
    arm_contours = []

    #contour masking
    diff = make_black(cv2.absdiff(frame1, frame2))
    gray= cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    b, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, b = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ######
    MOTION_DETECTED = False
    for contour in contours:
        area=cv2.contourArea(contour)
        if area<500:#shuttle
            shuttle_contours.append(contour)
        elif 2000<area<8000: #hopefully arm
            arm_contours.append(contour)

    for contour in shuttle_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red box for shuttle
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        print(f"Shuttle detected at {timestamp:.2f} seconds")

    for contour in arm_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box for arm
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        #print(f"body detected at {timestamp:.2f} seconds")
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
    #cv2.imwrite(f"{OUTPUT_DIR}/frame_{frame_count}.jpg", frame1) #to save shuttle detected scenes
    cv2.imshow("Motion Detection", diff) # change to diff to see filtered
    frame1 = frame2
    ret, frame2 = cap.read()
    frame_count+=1
    if cv2.waitKey(30) & 0xFF == 27:  # esc to exit
        break


cap.release()
cv2.destroyAllWindows()

