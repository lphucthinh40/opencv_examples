import cv2
import argparse
import numpy as np

# Use default image: python submission.py
# For custom image: python submission.py -p {image-path}

class BlemishRemover:
    def __init__(self):
        self.radius = 16

    def loadImage(self, image):
        self.img = image
        self.edited_img = np.copy(image)
        self.height, self.width, self.channel = image.shape
    
    def process(self, x, y):
        x0, x1 = max(0,x-self.radius), min(self.width, x+self.radius)
        y0, y1 = max(0,y-self.radius), min(self.height, y+self.radius)
        target_roi = self.img[y0:y1, x0:x1]
        delta_x, delta_y = x1 - x0, y1 - y0
        # checking four nearby ROIs (left, right, top, bottom)
        sobelx = cv2.Sobel(target_roi,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(target_roi,cv2.CV_64F,0,1,ksize=3)     
        sobel_min = np.mean(np.absolute(sobelx) + np.absolute(sobely))
        nearby_rois = np.array([[x0-delta_x-1, x0-1, y0, y1],
                                [x1+1, x1+delta_x+1, y0, y1],
                                [x0, x1, y0-delta_y-1, y0-1],
                                [x0, x1, y1+1, y1+delta_y+1]
                               ])
        best_idx = -1
        for idx, roi in enumerate(nearby_rois):
            if (roi[0]<0) or (roi[1]>self.width) or (roi[2]<0) or (roi[3]>self.height):
                continue
            temp_roi = self.img[roi[2]:roi[3], roi[0]:roi[1]]
            sobelx = cv2.Sobel(temp_roi,cv2.CV_64F,1,0,ksize=3)
            sobely = cv2.Sobel(temp_roi,cv2.CV_64F,0,1,ksize=3)
            sobel_score = np.mean(np.absolute(sobelx) + np.absolute(sobely))
            # pick roi with the least activity
            if (sobel_min > sobel_score):
                sobel_min = sobel_score
                best_idx = idx
        # perform seamless cloning
        if best_idx != -1:
	        x2, x3, y2, y3 = nearby_rois[best_idx]
	        best_roi = self.img[y2:y3, x2:x3]
	        mask = np.ones_like(target_roi, dtype = np.uint8) * 255
	        center = (delta_x//2, delta_y//2)
	        edited_roi = cv2.seamlessClone(best_roi, target_roi, mask, center, cv2.NORMAL_CLONE)
	        self.edited_img[y0:y1, x0:x1] = edited_roi

DEFAULT_IMAGE = "./blemish.png"
br = BlemishRemover()

def edit(action, x, y, flags, userdata):
	global br
	if action==cv2.EVENT_LBUTTONDOWN:
		# remove blemish
		br.process(x, y)

def main(image_path):
	global br
	img = cv2.imread(image_path, 1)
	br.loadImage(img)
	cv2.namedWindow("MainWindow")
	cv2.setMouseCallback("MainWindow", edit)
	k=0
	# wait for escape key
	while k!=27:
		cv2.imshow("MainWindow", br.edited_img)
		k = cv2.waitKey(20) & 0xFF
	# save edited image before exit
	cv2.imwrite(f"edited.png", br.edited_img)

if __name__ == '__main__':
	ap = argparse.ArgumentParser(description='Image Annotation App')
	ap.add_argument('-p', metavar='P', type=str, help='path to image file', default=DEFAULT_IMAGE)
	args = ap.parse_args()
	
	main(args.p)