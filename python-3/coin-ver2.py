import cv2
import numpy as np
import matplotlib.pyplot as plt

# Image Read
src = cv2.imread('coins1.jpg')

# Convert Image to Gray
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# Apply Gaussian filter
blr = cv2.GaussianBlur(gray, (0, 0), 1)

# Circle detection
circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 30, param1=130, param2=40, minRadius=15, maxRadius=100)

sum_of_money = 0
dst = src.copy()

# Output Results
if circles is not None:
    for i in range(circles.shape[1]):
        cx, cy, radius = circles[0][i]

        # Extract the area of the coin
        x1 = int(cx - radius)
        y1 = int(cy - radius)
        x2 = int(cx + radius)
        y2 = int(cy + radius)
        radius = int(radius)

        crop = dst[y1:y2, x1:x2, :]
        ch, cw = crop.shape[:2]

        # Create ROI Mask
        mask = np.zeros((ch, cw), np.uint8)
        cv2.circle(mask, (cw//2, ch//2), radius, 255, -1)

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        hue, _, _ = cv2.split(hsv)
        hue_shift = (hue + 40) % 180
        mean_of_hue = cv2.mean(hue_shift, mask)[0]

        # Classification of 10 won and 100 won
        won1 = 100
        won2 = 10
        if mean_of_hue < 90:
            cv2.circle(dst, (int(cx), int(cy)), int(radius), (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(crop, str(won2), (23,25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2, cv2.LINE_AA)
            sum_of_money+=won2
            # Circle center coordinates
            cv2.putText(crop, f'({cx},{cy})', (3,60),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1, cv2.LINE_AA)
        else:
            cv2.circle(dst, (int(cx), int(cy)), int(radius), (255,0,0), 2, cv2.LINE_AA)
            cv2.putText(crop, str(won1), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), 2, cv2.LINE_AA)
            sum_of_money+=won1
            # Circle center coordinates
            cv2.putText(crop, f'({cx},{cy})', (15,75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1, cv2.LINE_AA)

# Find the center of the circle
if circles is not None:
    circles=np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(dst, (i[0], i[1]), 2, (0, 255, 0), 5)

# Design
font={'family' : 'serif', 'color' : 'black', 'weight' : 'bold', 'size' : 18}
title_font={'fontweight' : 'bold', 'family' : 'serif'}

plt.figure("Team 7 - geumjjogi", figsize=(20,20))
plt.subplot(1,1,1)
plt.title('Result', fontsize=45, pad = 15, fontdict = title_font)
plt.text(0.1, 0.1, f'Sum : {sum_of_money}won', fontdict=font, horizontalalignment='left', verticalalignment='bottom')
plt.imshow(dst)
plt.show()
