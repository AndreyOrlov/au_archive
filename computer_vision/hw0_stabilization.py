import cv2
import numpy as np

def findHomography(im0, im1):
    fd = cv2.FastFeatureDetector(10)
    fs = fd.detect(im0)
    fs = np.float32([x.pt for x in fs])
    nfs, s, te = cv2.calcOpticalFlowPyrLK(im0, im1, fs, None, (121,121))
    #fs = fs[reshape(s > 0, s.size)]
    #nfs = nfs[reshape(s > 0, s.size)]
    return cv2.findHomography(fs, nfs, cv2.RANSAC)



def videoReadTest():
    vc = cv2.VideoCapture('/home/andrey/cv_test/test_stable.avi')
    isRead, initFrame = vc.read()
    w = len(initFrame[0])
    h = len(initFrame)
    writer = cv2.VideoWriter('out_stable.avi', cv2.cv.CV_FOURCC(*'MJPG'), 30.0, (w, h), True)
    while True:
        isRead, frame = vc.read()
        if not isRead :
            break
        H, mask = findHomography(frame, initFrame)
        warped = cv2.warpPerspective(frame, H, (w,h))
        
        writer.write(warped)

if __name__ == '__main__':
    videoReadTest()