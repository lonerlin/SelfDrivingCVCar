import cv2
import time
import numpy as np







def nothing(x):
    pass


def trackshow(source=1, ksize=5, interv=5 ):
    tic = time.time()
    tic1 = time.time()
    coords = []

    # open stream, capture image
    # stream = cv.CaptureFromCAM(source)
    cap = cv2.VideoCapture(source)

    cv2.namedWindow('control')
    tracker = np.zeros((640, 480))

    cv2.createTrackbar('Hlow', 'control', 0, 255, nothing)
    cv2.createTrackbar('Hhigh', 'control', 60, 255, nothing)
    cv2.createTrackbar('Llow', 'control', 0, 255, nothing)
    cv2.createTrackbar('Lhigh', 'control', 60, 255, nothing)
    cv2.createTrackbar('Slow', 'control', 50, 255, nothing)
    cv2.createTrackbar('Shigh', 'control', 255, 255, nothing)

    while True:
        # img_now = cv.QueryFrame(stream)
        _, frame = cap.read()

        # to HSV. Try use HSL / HLS?
        hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # get current positions of the trackbars
        hl = cv2.getTrackbarPos('Hlow', 'control')
        hh = cv2.getTrackbarPos('Hhigh', 'control')
        ll = cv2.getTrackbarPos('Llow', 'control')
        lh = cv2.getTrackbarPos('Lhigh', 'control')
        sl = cv2.getTrackbarPos('Slow', 'control')
        sh = cv2.getTrackbarPos('Shigh', 'control')

        # color masking: define color range
        lower = np.array([hl, ll, sl], dtype=np.uint8)
        upper = np.array([hh, lh, sh], dtype=np.uint8)
        mask = cv2.inRange(frame, lower, upper)
        cv2.imshow("mask", mask)
        print(np.sum(mask == 255))
        # morphological opening: erode and dilate
        # kernel = np.ones((ksize, ksize), np.uint8)
        # eroded = cv2.erode(mask, kernel)
        # dilated = cv2.dilate(eroded, kernel)
        #
        # # morphological closing: dilate and erode
        # dilated = cv2.dilate(dilated, kernel)
        # closed = cv2.erode(dilated, kernel)
        #
        # # result: mask & original image:
        # res = cv2.bitwise_and(frame, frame, mask=closed)
        #
        # x = np.sum(res == 255)
        # print(x)
        # # get contour
        # _,conts, hier = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # # find longest contour
        # maxArea = 0
        # cxs = []
        # cys = []
        # for i in range(len(conts)):
        #     if hier[0][i][3] == -1:
        #         newArea = cv2.contourArea(conts[i])
        #         if newArea > maxArea:
        #             maxcont = conts[i]
        #             maxArea = newArea
        #
        # if len(conts) > 0:
        #     cv2.drawContours(res, maxcont, -1, (0, 255, 0), 5)
        #
        #     # centroid position from the moments
        #     mom = cv2.moments(maxcont)
        #     cx = int(mom['m10'] / mom['m00'])
        #     cy = int(mom['m01'] / mom['m00'])
        #     # draw centroid
        #     cv2.circle(res, (cx, cy), 5, (255, 0, 0), -1)
        #
        #     # keep track of last 5
        #     cxs = [cx] + cxs[1:]
        #     cys = [cy] + cys[1:]
        #
        # if time.time() - tic > interv:
        #     tic = time.time()
        #     if len(cxs) > 0:
        #         x, y = np.mean(cxs), np.mean(cy)
        #         t = time.time() - tic1
        #         coords.append([t, x, y])
        #         tracker[x, y] += .2

        #build a window
        cv2.imshow('control',tracker)
        cv2.imshow('original', frame)
         # cv2.imshow('result', res)
        #cv2.imshow('tracker', tracker)
        #

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

if __name__ =='__main__':
    trackshow(0)

    cv2.destroyAllWindows()