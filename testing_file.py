import cv2
import time
from imutils.video import VideoStream
import matplotlib.pyplot as plt

cap = VideoStream(src=1).start()
time.sleep(1.0)
cap = cv2.VideoCapture(0)
ok, frame = cap.read()
print(ok)

bbox = cv2.selectROI(frame)
(x, y, w, h) = bbox
track_window = (x, y, w, h)
print(track_window)

roi = frame[y:y+h, x:x+w]
#cv2.imshow('ROI', roi)
#cv2.waitKey(0)
hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
#cv2.imshow('ROI HSV', hsv_roi)
#cv2.waitKey(0)

roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0,180])

plt.hist(roi.ravel(), 180, [0, 180])
#plt.show()
#cv2.waitKey(0)

roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

parameters = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ok, frame = cap.read()
    if ok == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)
        ok, track_window = cv2.meanShift(dst, (x, y, w, h), parameters)

        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Meanshift tracking', frame)
        cv2.imshow('dst', dst)
        cv2.imshow('ROI', roi)

        if cv2.waitKey(1) == 13: # esc
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()
