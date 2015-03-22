import cv2
import numpy as np

def getFields():
    fields = []
    k = 420 / 8
    for y in xrange(8):
        for x in xrange(8):
            if x % 2 != y % 2:
                pt1 = (k*x, k*y)
                pt2 = (k*x + k, k*y + k)
                fields.append([pt1, pt2, 0])
    return fields

def getWhiteAwg(warp, fields):
    whiteAvg = np.float32(warp[fields[0][0][0]:fields[0][1][0], fields[0][0][1]:fields[0][1][1]])
    for i in xrange(21, 32):
        field = warp[fields[i][0][0]:fields[i][1][0], fields[i][0][1]:fields[i][1][1]]
        cv2.accumulateWeighted(field, whiteAvg, 0.1)
    return cv2.convertScaleAbs(whiteAvg)

def getBlackAvg(warp, fields):
    wp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    blackAvg = np.float32(wp[fields[0][0][1]+20:fields[0][1][1]-10, fields[0][0][0]+15:fields[0][1][0]-15])
    for i in xrange(0, 12):
        field = wp[fields[i][0][1]+20:fields[i][1][1]-10, fields[i][0][0]+15:fields[i][1][0]-15]
    cv2.accumulateWeighted(field, blackAvg, 0.1)

    return cv2.convertScaleAbs(blackAvg)

def whiteDetect(fields, oldfields, warp, whiteAvg):
    minSize = 38
    for i in xrange(32):
        field = warp[fields[i][0][0]:fields[i][1][0], fields[i][0][1]:fields[i][1][1]]
        diff = cv2.absdiff(field, whiteAvg)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 45,  0xff, cv2.THRESH_BINARY)
        weight = np.sum(mask)
        if 290000 <= weight <= 480000 and oldfields[i][2] != 1:
            fields[i][2] = 2
        #print i, "--", weight
        #for j,k in np.argwhere(mask == 0xff):
        #    if mask[j, k] == 0xff:
        #        _, obj = cv2.floodFill(mask, None, (k, j), 30)
        #        if obj[2] * obj[3] >= minSize * minSize and (obj[2] > minSize or obj[3] > minSize):
        #            print i, np.sum(mask) # 43000 80000
        #            fields[i][2] = 2
    return fields

def blackDetect(fields, oldfields, warp, blackAvg):
    wp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    for i in xrange(32):
        field = wp[fields[i][0][0]+20:fields[i][1][0]-10, fields[i][0][1]+15:fields[i][1][1]-15]
        mask = cv2.absdiff(field, blackAvg)
        _, mask = cv2.threshold(mask, 15,  0xff, cv2.THRESH_BINARY_INV)
        weight = np.sum(mask)
        if weight > 105000:
            fields[i][2] = 1

        elif oldfields[i][2] != 1:
            continue
        a, b, c, d = 0, 0, 0, 0
        if i % 8 < 4:
            j, k = i + 4, i + 5
            l, m = i - 3, i - 4
        else:
            j, k = i + 3, i + 4
            l, m = i - 5, i - 4
        if j > 31 or oldfields[j][2] == 1:
            a = 1
        if k > 31 or oldfields[k][2] == 1:
            b = 1
        if l < 0 or oldfields[l][2] == 1:
            c = 1
        if m < 0 or oldfields[m][2] == 1:
            d = 1
        if a == 1 and b == 1 and c == 1 and d == 1:
            fields[i][2] = 1
    return fields

def main(filename):
    vc = cv2.VideoCapture(filename)
    writer = cv2.VideoWriter('/home/andrey/cv_test/checkers_out.avi', cv2.cv.CV_FOURCC(*'MJPG'), 15, (420, 420), True)
    fields = getFields()
    for f in xrange(4000):
        isRead, frame = vc.read()
        if not isRead:
            break
        p1 = np.float32([[10, 10], [10, 400], [400, 10], [400, 400]])
        p2 = np.float32([[160,115], [95,305], [484,110], [550,300]])

        H, _ = cv2.findHomography(p2, p1, cv2.RANSAC)
        warp = cv2.warpPerspective(frame, H, (420, 420))
        if f == 0:
            whiteAvg = getWhiteAwg(warp, fields)
            blackAvg = getBlackAvg(warp, fields)
        if f % 15 == 0:
            oldfields = fields
            fields = getFields()
            fields = whiteDetect(fields, oldfields, warp, whiteAvg)
            fields = blackDetect(fields, oldfields, warp, blackAvg)

        desk = np.zeros((420, 420, 3), np.uint8)
        cv2.rectangle(desk, (0, 0), (420, 420), (128, 128, 128), -1)
        for i in xrange(len(fields)):
            cv2.rectangle(desk, fields[i][1], fields[i][0], (0, 0, 0), -1)
        for i in xrange(len(fields)):

            x = (fields[i][0][1] + fields[i][1][1]) / 2
            y = (fields[i][0][0] + fields[i][1][0]) / 2
            if fields[i][2] == 1:
                cv2.circle(desk, (x, y), 14, cv2.cv.CV_RGB(0, 0, 255), 10)
            elif fields[i][2] == 2:
                cv2.circle(desk, (x, y), 14, cv2.cv.CV_RGB(255, 0, 0), 10)
        newimg = np.zeros((420, 840, 3), np.uint8)
        newimg[:420, :420] = warp
        newimg[:420, 420:840] = desk
        cv2.imshow('window', newimg)
        cv2.waitKey(10)
        writer.write(newimg)


if __name__ == '__main__':
    main("checkers.mp4")
