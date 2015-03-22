import cv2
import numpy as np

def getKP(img1, img2, threshold):
    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")
    kp1 = detector.detect(img1)
    kp1, d1 = descriptor.compute(img1, kp1)
    kp2 = detector.detect(img2)
    kp2, d2 = descriptor.compute(img2, kp2)
    flann_params = dict(algorithm = 1, trees = 4)
    flann = cv2.flann_Index(d1, flann_params)
    idx, dist = flann.knnSearch(d2, 2, params = {})
    kp1_result = []
    kp2_result = []
    for i in xrange(len(dist)):
        if dist[i][0] / dist[i][1] < threshold:
            kp1_result.append(kp1[idx[i][0]])
            kp2_result.append(kp2[i])
    return kp1_result, kp2_result

def getImg(img1, img2, H):
    h1, w1 = img1.shape[ : 2]
    h2, w2 = img2.shape[ : 2]
    warp = cv2.warpPerspective(img2, H, (w1 + w2, h1))
    warp[ : h1, : w1] = img1[ : h1, : w1]
    w = w1 + w2 - 1
    while(w > 0 and (warp[0, w] == [0, 0, 0]).all()):
        w -= 1
    return warp[ : h1, : w]

def gluing(filename1, filename2):
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    kp1, kp2 = getKP(img1, img2, 0.5)
    p1 = np.float32([kp1[i].pt for i in xrange(len(kp1))])
    p2 = np.float32([kp2[i].pt for i in xrange(len(kp2))])
    print (p1)
    H, _ = cv2.findHomography(p2, p1, cv2.RANSAC)
    img = getImg(img1, img2, H)
    cv2.imshow('window', img)
    cv2.waitKey()


if __name__ == '__main__':
    gluing("part1.jpg", "part2.jpg")
