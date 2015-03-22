import cv2
import numpy as np

def sortDist(idx, dist):
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i][0])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    return idx, dist

def getDescriptors(img1, img2):
    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")

    kp1 = detector.detect(img1)
    kp1, d1 = descriptor.compute(img1, kp1)

    kp2 = detector.detect(img2)
    kp2, d2 = descriptor.compute(img2, kp2)
    return  kp1, d1, kp2, d2

def findKeyPointsMinDist(kp1, d1, kp2, d2):
    matcher = cv2.DescriptorMatcher_create('BruteForce')
    raw_matches = matcher.knnMatch(d1, d2, 2)
    kp1_result = []
    kp2_result = []
    for m in raw_matches:
        if len(m) == 2 and m[0].distance < m[1].distance * 0.5:
            m = m[0]
            kp1_result.append( kp1[m.queryIdx] )
            kp2_result.append( kp2[m.trainIdx] )
    return kp1_result, kp2_result

def findKeyPointsEps(kp1, d1, kp2, d2, epsilon=1):
    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(d1, flann_params)
    idx, dist = flann.knnSearch(d2, 2, params={})
    kp1_result = []
    kp2_result = []
    for i in xrange(len(kp1)):
        if dist[i][0] / dist[i][1] < epsilon:
            kp1_result.append(kp1[idx[i][0]])
            kp2_result.append(kp2[i])

    return kp1_result, kp2_result

def drawKeyPoints(img1, img2, kp1, kp2, num):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    nWidth = w1 + w2
    nHeight = max(h1, h2)
    hdif = (h1 - h2) / 2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif + h2, :w1] = img1
    newimg[:h1, w1:w1+w2] = img2

    maxlen = min(len(kp1), len(kp2))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in xrange(num):
        pt_a = (int(kp2[i].pt[0]+w1), int(kp2[i].pt[1]))
        pt_b = (int(kp1[i].pt[0]), int(kp1[i].pt[1]))
        if abs (kp1[i].pt[0]- kp2[i].pt[1]) < 100 and abs(kp1[i].pt[1] - w1 + kp2[i].pt[0]) < 100:
            cv2.line(newimg, pt_a, pt_b, ((i * 13) % 255, (i * 53) % 255, (i * 29) % 255), 2)
            cv2.circle(newimg, pt_a, 3,  ((i * 13) % 255, (i * 53) % 255, (i * 29) % 255), 3)
            cv2.circle(newimg, pt_b, 3,  ((i * 13) % 255, (i * 53) % 255, (i * 29) % 255), 3)

    return newimg

def stat (kp1, kp2, width):
    matched = 0
    for i in xrange(min(len(kp1), len(kp2))):
        if abs (kp1[i].pt[0]- kp2[i].pt[1]) < 20 and abs(kp1[i].pt[1] - width + kp2[i].pt[0]) < 20:
            matched += 1
    return matched

def SIFT_test(filename1, filename2):
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    width = len(img1)
    eps = 1
    num = -1

    kp1, d1, kp2, d2 = getDescriptors(img1, img2)

    p1, p2 = findKeyPointsMinDist(kp1, d1, kp2, d2)
    newImg = drawKeyPoints(img1, img2, p1, p2, num)
    cv2.imshow("Using Min Dist", newImg)
    matched = stat(p1, p2, width)
    print "Matched key point using min dist", matched, "of",len(kp1)
    p1, p2 = findKeyPointsEps(kp1, d1, kp2, d2, eps)
    newImg = drawKeyPoints(img1, img2, p1, p2, num)
    matched = stat(p1, p2, width)
    print "Matched key point using two min dist", matched, "of",len(kp1)
    cv2.imshow("Using Epsilon", newImg)
    cv2.waitKey(0)

if __name__ == '__main__':
    SIFT_test('castle.jpg', 'castle_90.jpg')
