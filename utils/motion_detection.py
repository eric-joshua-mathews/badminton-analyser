import cv2
import os
import numpy as np
#roi_points = []
def make_black(frame):
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    mask_inv = cv2.bitwise_not(mask)
    blacked_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
    return blacked_frame

# def mousecallback(event,x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         roi_points.append((x, y))
#         cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
#         print(f"Mouse clicked at ({x}, {y})")
#         cv2.imshow("ROI Selection", img)

VIDEO_PATH = 'Rallies/Rally1.mov'
OUTPUT_DIR = 'Outputs'
MIN_AREA=5000
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# #user selects ROI
# img=frame1.copy()
# cv2.imshow("Select ROI", img)
# mousecallback("Select ROI",img)

frame_count=0

while ret:
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
        print(f"Arm detected at {timestamp:.2f} seconds")
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
    cv2.imwrite(f"{OUTPUT_DIR}/frame_{frame_count}.jpg", frame1)
    cv2.imshow("Motion Detection", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    frame_count+=1
    if cv2.waitKey(30) & 0xFF == 27:  # esc to exit
        break


cap.release()
cv2.destroyAllWindows()

