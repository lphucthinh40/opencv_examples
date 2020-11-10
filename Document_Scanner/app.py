import cv2
import argparse
import numpy as np

from scanner import DocumentScanner
from scanner import resize_image

# Use default image: python submission.py
# For custom image: python submission.py -p {image-path}

# ASCII code
SPACE_KEY = 32
ESCAPE_KEY = 27

# UI Preset Constants
DEFAULT_IMAGE = "./scanned-form.jpg"
WINDOW_NAME = "Document Scanner"
DISPLAY_HEIGHT = 960
MOUSE_RADIUS = 5

# Global Variables
ds = DocumentScanner()
resized_image = None
corners = None
edited_image = None
target_corner = -1
app_state = 0

def mouse_handler(action, x, y, flags, param):
	# handle mouse actions and update corners
	global ds, resized_image, corners, target_corner, edited_image
	if app_state == 0:
		if action==cv2.EVENT_LBUTTONDOWN:
			# select corner
			point = np.array([x , y], np.int32)
			# target_corner = -1
			for i in range(len(corners)):
				dist = np.linalg.norm(corners[i]-point)
				if dist < MOUSE_RADIUS:
					target_corner = i
					break
		elif action == cv2.EVENT_MOUSEMOVE:
			if target_corner != -1:
				point = np.array([x , y], np.int32)
				corners[target_corner, :] = point
				edited_image = ds.drawPolyRegion(resized_image, corners) 
				cv2.imshow(WINDOW_NAME, edited_image)
		elif action == cv2.EVENT_LBUTTONUP:
			target_corner = -1


def main(image_path):
	global ds, corners, edited_image, original_image, resized_image, app_state

	# load image
	original_image = cv2.imread(image_path, 1)
	resized_image, ratio = resize_image(original_image, height = DISPLAY_HEIGHT)
	corners = ds.scan(resized_image)
	edited_image = ds.drawPolyRegion(resized_image, corners)
	cv2.putText(edited_image,"Adjust corners with your LEFT MOUSE",
	            (10,20), cv2.FONT_HERSHEY_SIMPLEX,
	            0.75,(255,255,255), 1 )
	cv2.putText(edited_image,"Press SPACE to extract document. Press ESC to exit",
                (10,50), cv2.FONT_HERSHEY_SIMPLEX,
                0.75,(255,255,255), 1 )
	# setup OpenCV window
	cv2.namedWindow(WINDOW_NAME)
	cv2.setMouseCallback(WINDOW_NAME, mouse_handler)
	k=0
	# wait for escape key
	while k!=ESCAPE_KEY:
		# handle space key
		if (k==SPACE_KEY):
			if (app_state==0):
				warped_image = ds.transform(resized_image, corners)
				edited_image = warped_image.copy()
				cv2.putText(edited_image,"Press ESC to save and exit. Press SPACE to apply thresholding",
                    (5,25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,(255,0,0), 1 )
				app_state=1
			elif (app_state==1):
				thresh = ds.threshold(warped_image)
				edited_image = cv2.merge((thresh, thresh, thresh))
				cv2.putText(edited_image,"Press ESC to save and exit",
                    (5,25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,(255,0,0), 1 )
				app_state=2
		cv2.imshow(WINDOW_NAME, edited_image)
		
		k = cv2.waitKey(20) & 0xFF
	# save edited image before exit
	corners = (corners / ratio).astype(np.int32)
	warped = ds.transform(original_image, corners)
	if app_state==1:
		cv2.imwrite(f"document.jpg", warped)
	elif app_state==2:
		thresh = ds.threshold(warped)
		cv2.imwrite(f"thresholded_document.jpg", thresh)

	print("extracted document saved")

if __name__ == '__main__':
	ap = argparse.ArgumentParser(description='Image Annotation App')
	ap.add_argument('-p', metavar='P', type=str, help='path to image file', default=DEFAULT_IMAGE)
	args = ap.parse_args()
	
	main(args.p)