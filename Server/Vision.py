import math
import cv2
import numpy as np
from PIL import Image, ImageFilter

SAT_MIN, SAT_MAX = 30,  256
HUE_MIN, HUE_MAX = 230, 10
VAL_MIN, VAL_MAX = 20,  256

def get_corners(orig_img):
    filter_ = ImageFilter.GaussianBlur(radius=3) 
    blurred_image = orig_img.filter(filter_)
    img = blurred_image.convert("HSV")
    hue = np.array(img)[:, :, 0]
    sat = np.array(img)[:, :, 1]
    val = np.array(img)[:, :, 2]
    mask  = ((hue > HUE_MIN) | (hue < HUE_MAX))
    mask &= (sat > SAT_MIN) & (sat < SAT_MAX)
    mask &= (val > VAL_MIN) & (val < VAL_MAX)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 20
    params.maxArea = 100000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = True
    params.blobColor = 255

    is_cv3 = cv2.__version__.startswith("3.")
    if is_cv3:
        detector = cv2.SimpleBlobDetector_create(params)
    else:
        detector = cv2.SimpleBlobDetector(params)
    keypoints = detector.detect((mask*255).astype(np.uint8))
    print("Number of detected blobs ", len(keypoints))

    if len(keypoints) != 4:
        return None, None, None


    center_x, center_y = 0, 0
    for i in range(4):
        center_x += keypoints[i].pt[0]
        center_y += keypoints[i].pt[1]
    center_x /= 4
    center_y /= 4

    tl, tr, bl, br = 0, 0, 0, 0
    for i in range(4):
        if keypoints[i].pt[0] < center_x and keypoints[i].pt[1] < center_y:
            tl = np.array([keypoints[i].pt[0], keypoints[i].pt[1]])
        if keypoints[i].pt[0] < center_x and keypoints[i].pt[1] > center_y:
            bl = np.array([keypoints[i].pt[0], keypoints[i].pt[1]])
        if keypoints[i].pt[0] > center_x and keypoints[i].pt[1] < center_y:
            tr = np.array([keypoints[i].pt[0], keypoints[i].pt[1]])
        if keypoints[i].pt[0] > center_x and keypoints[i].pt[1] > center_y:
            br = np.array([keypoints[i].pt[0], keypoints[i].pt[1]])

    rect = np.array([tl, tr, bl, br]).astype(np.float32)
    scale = 4
    t, b, l, r = -8, 106, -8, 107

    t *= scale
    b *= scale
    l *= scale
    r *= scale

    dst = np.array(
        [(l, t),
        (r, t),
        (l, b),
        (r, b)]).astype(np.float32)
    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(np.array(orig_img), M, (int(100 * scale), int(100 * scale)))
    print(M)
    M_inv = np.linalg.inv(M)
    centers = np.zeros((8, 8, 2))
    for i in range(8):
        for j in range(8):
            v = np.matmul(M_inv, np.array([i * 50 + 25, j * 50 + 25, 1]))
            centers[i,j,0] = v[0] / v[2]
            centers[i,j,1] = v[1] / v[2]
    corners = np.zeros((9, 9, 2))
    for i in range(9):
        for j in range(9):
            v = np.matmul(M_inv, np.array([i * 50, j * 50, 1]))
            corners[i,j,0] = v[0] / v[2]
            corners[i,j,1] = v[1] / v[2]
    # print(centers)


    gray = cv2.cvtColor(warp, cv2.COLOR_RGB2GRAY)
    
    ave_array = []
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                ave = np.average(gray[i * 50:i*50 + 50,j*50:j*50+50])
                ave_array.append(ave)
    ave_array = sorted(ave_array)
    ave_median = ave_array[16]
    ave_max = ave_array[31]

    matrix = np.zeros((8, 8))
    # Some hardcoded detection, that assumes there are white pieces:
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                ave = np.average(gray[i * 50:i*50 + 50,j*50:j*50+50])
                if ave < ave_median - 30:
                    matrix[i,j] = 2
                if ave > ave_max - 15:
                    matrix[i,j] = 1

    print(matrix)
    return (corners, matrix, centers)


if __name__ == "__main__":
    img = Image.open("/Users/KOCABEY/Desktop/ebucehil.JPG")
    print(get_corners(img))
