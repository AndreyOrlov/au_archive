import cv2

def filters_test(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    src = img.copy()
    noise = img.copy()
    cv2.randn(noise, 5, 10)
    cv2.add(src, noise, src)
    cv2.imshow("origin", src)

    # Gaussian Blur
    dst = src.copy()
    dst2 = src.copy()
    cv2.GaussianBlur(src, (3, 3), 0 ,dst)
    cv2.imshow("GaussianBlur", dst)
    cv2.absdiff(img, dst, dst2)
    cv2.imshow("GaussianBlur diff", dst2)

    # Bilateral Blur
    dst = src.copy()
    dst2 = src.copy()
    cv2.bilateralFilter(src, 15, 20, 5, dst)
    cv2.imshow("Bilateral filter", dst)
    cv2.absdiff(img, dst, dst2)
    cv2.imshow("Bilateral filter diff", dst2)

    # Nonlocal means filter
    dst = src.copy()
    dst2 = src.copy()
    cv2.fastNlMeansDenoising(src, dst, 5, 5)
    cv2.imshow("Nonlocal means filter", dst)
    cv2.absdiff(img, dst, dst2)
    cv2.imshow("Nonlocal means filter diff", dst2)

    cv2.waitKey()

if __name__ == '__main__':
    filters_test('cameraman.jpg')
