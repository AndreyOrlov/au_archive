import cv2
import  numpy as np
def circle_detection(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(img, (3, 3), 0 ,img)
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 10, param1 = 100)
    circles = np.uint16(np.around(circles))
    for circle in circles[0]:
        cv2.circle(img, (circle[0], circle[1]), circle[2], (128, 0, 0), 3)
    cv2.imshow("window", img)
    cv2.waitKey(0)

if __name__ == '__main__':
    circle_detection("circles.jpg")