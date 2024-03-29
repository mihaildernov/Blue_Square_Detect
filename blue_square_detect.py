import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bl = cv2.medianBlur(gr, 5)
    canny = cv2.Canny(bl, 10, 250)
    kernal = np.ones((5, 5), "uint8")

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, frame,
                               mask=blue_mask)

    contours = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

    for cont in contours:
        area = cv2.contourArea(cont)

        if area > 10000:
            sm = cv2.arcLength(cont, True)
            apd = cv2.approxPolyDP(cont, 0.02 * sm, True)

            if len(apd) == 4:
                cv2.drawContours(frame, [apd], -1, (0, 255, 0), 4)
                print("Обнаружен синий квадрат")

            centres = []
            x1 = 320; y1 = 240

            moment = cv2.moments(cont)
            x2 = int(moment['m10'] / moment['m00']); y2 = int(moment['m01'] / moment['m00'])
            centres.append((x2, y2))
            x = x2 - x1; y = y2 - y1
            print(centres)
            print()

    cv2.imshow("Blue Square Detection", frame)

    if cv2.waitKey(1) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()
