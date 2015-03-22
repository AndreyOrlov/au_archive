import cv2
import numpy as np

def calcBkg(bkgWindow):
    avg1 = np.float32(bkgWindow[0])
    for i in (xrange(1, len(bkgWindow))):
        cv2.accumulateWeighted(bkgWindow[i] ,avg1, 0.1)
             
    return cv2.convertScaleAbs(avg1)

def precalcBkg(filename):
    vc = cv2.VideoCapture(filename)
    _, frame = vc.read()
    avg = np.float32(frame)
    while True:
        isRead, frame = vc.read()
        if not isRead:
            break
        cv2.accumulateWeighted(frame ,avg, 0.1)
    return cv2.convertScaleAbs(avg)

def initBkgWindow(size, filename):
    res = []
    vc = cv2.VideoCapture(filename)
    for i in xrange(size):
        isRead, frame = vc.read()
        if not isRead:
            break
        res.append(frame)
    return res

def getMask(frame, bkg, threshold):
    kernel = np.ones((8, 8), 'uint8')
    diff = cv2.absdiff(frame, bkg)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, threshold,  0xff, cv2.THRESH_BINARY)
    mask = cv2.dilate(mask, kernel)
    return mask
    
def findFrameObjects (mask, minSize):
    objects = []
    curColor = 1
    for i, j in np.argwhere(mask == 0xff):
        if mask[i, j] == 0xff:
            _, obj = cv2.floodFill(mask, None, (j, i), curColor)
            curColor += 1
            if obj[2] * obj[3] >= minSize * minSize and (obj[2] > minSize or obj[3] > minSize):
                objects.append(obj)
    return objects

def motionDetect(filename):
    #bkgWindow = initBkgWindow(100, filename)
    #bkgIdx = 0
    print "Precalc Background..."
    bkg = precalcBkg(filename)
    print "Motion detection..."
    vc = cv2.VideoCapture(filename)
    w = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)) 
    h = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter('/home/andrey/cv_test/out.avi', cv2.cv.CV_FOURCC(*'MJPG'), 15, (w, h), True)

    while True:
        isRead, frame = vc.read()
        #bkgWindow[bkgIdx] = frame
        #bkgIdx = (bkgIdx + 1) % len(bkgWindow)
        #bkg = calcBkg(bkgWindow)
        if not isRead:
            break
        mask = getMask(frame, bkg, 50)
        frameObjects = findFrameObjects(mask, int((w + h) * 0.02))
        for obj in frameObjects:
            pt1, pt2 = (obj[0], obj[1]), (obj[0] + obj[2], obj[1] + obj[3])
            cv2.rectangle(frame, pt1, pt2, cv2.cv.CV_RGB(255, 0, 0), 3)

        cv2.namedWindow('window', 0)
        cv2.imshow('window', frame)
        cv2.waitKey(10)
        writer.write(frame)
        
if __name__ == '__main__':
    motionDetect('Cam3_Outdoor.avi')
    
