import cv2
import numpy as np

def resize_image(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    r = 1
    
    if width is None and height is None:
        return image, r

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized, r

class DocumentScanner:
    def __init__(self):
        self.resize_length = 500
        self.blur_kernel = (9, 9)
        self.thresh_blocksize = 71
        self.thresh_c = 0
        self.approx_percent = 0.02
        self.letter_size_ratio = 1.294
        
    def scan(self, image):
        resized = image.copy()
        ratio = 1
        # resize image if necessary
        self.height, self.width, _ = image.shape
        if (self.height > 720):
            resized, ratio = resize_image(image, height = self.resize_length)
        elif (self.width > 720):
            resized, ratio = resize_image(image, width = self.resize_length)
        
        # convert to grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        # apply gaussian blur
        blur = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        # adaptive threshold
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, self.thresh_blocksize, self.thresh_c)
        # find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # sort contour based on its area
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        # approximate contour
        for cnt in contours:
            epsilon = self.approx_percent * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # we only need the first rectangle shape, which has the largest area
            if (len(approx)==4):
                break;
        # make sure four vertexs are in correct order (counter-clockwise)
        approx = np.squeeze(approx) / ratio
        approx = approx.astype(np.int32)
        approx = approx[np.argsort(approx[:, 0])] # sort on x-axis
        top_left     = approx[0,:] if approx[0,1]<=approx[1,1] else approx[1, :]
        bottom_left  = approx[1,:] if approx[0,1]<=approx[1,1] else approx[0, :]
        bottom_right = approx[2,:] if approx[2,1]>=approx[3,1] else approx[3, :]
        top_right    = approx[3,:] if approx[2,1]>=approx[3,1] else approx[2, :]
        rec = np.array([top_left, bottom_left, bottom_right, top_right])
        return rec
    
    def transform(self, image, points):
        h, w, c = image.shape
        ref_height, ref_width = int(w*self.letter_size_ratio), w
        ref_points = np.array([[0, 0],[0, ref_height-1],[ref_width-1, ref_height-1], [ref_width-1, 0]])
        h, mask = cv2.findHomography(points, ref_points, cv2.RANSAC)
        out_img = cv2.warpPerspective(image, h, (ref_width, ref_height))
        return out_img
    
    def threshold(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen = cv2.GaussianBlur(gray, (0,0), 3)
        sharpen = cv2.addWeighted(gray, 1.5, sharpen, -0.5, 0)
        thresh = cv2.adaptiveThreshold(sharpen,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,21,15)          
        return thresh

    def drawPolyRegion(self, image, points):
        mask = np.zeros_like(image)
        edited_image = image.copy()
        mask = cv2.fillPoly(mask, [points], [0,255,0])
        edited_image = cv2.addWeighted(edited_image, 0.8, mask, 0.2, 0)
        edited_image = cv2.polylines(edited_image, [points], 1, [0,255,0], 4)

        for pt in points:
            edited_image = cv2.circle(edited_image,tuple(pt), 5, (0,255,0), -1)

        return edited_image
