import cv2
import os.path

image_extensions = ['.jpg', '.jpeg', '.png']
video_extensions = ['.mp4']

class MediaHandler:

	def __init__(self, fg_path, bg_path, out_path):
		self.fg_ext = os.path.splitext(fg_path)[1]
		self.bg_ext = os.path.splitext(bg_path)[1]
		self.out_path = out_path
		self.finished = False
		self.bg_frame = None
		self.fg_frame = None
		# Load foreground media
		if self.fg_ext in image_extensions:
			self.fg_frame = cv2.imread(fg_path)
		elif self.fg_ext in video_extensions:
			self.fg_cap = cv2.VideoCapture(fg_path)
			if (self.fg_cap.isOpened()== False): 
				print(f"Error opening video file: {fg_path}")
		else:
			print("Invalid file extension for foreground")
		# Load background media
		if self.bg_ext in image_extensions:
			self.bg_frame = cv2.imread(bg_path)
		elif self.bg_ext in video_extensions:
			self.bg_cap = cv2.VideoCapture(bg_path)
			if (self.bg_cap.isOpened()== False): 
				print(f"Error opening video file {bg_path}")
		else:
			print("Invalid file extension for background")
		# Decide Output Mode
		if self.bg_ext in video_extensions or self.fg_ext in video_extensions:
			self.output_type = 'video'
			if (self.fg_ext in video_extensions):
				self.reference = 'foreground'
				self.w, self.h = int(self.fg_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.fg_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				self.frame_rate = int(self.fg_cap.get(cv2.CAP_PROP_FPS))
			else:
				self.w, self.h = int(self.bg_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.bg_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
				self.reference = 'background'
				self.frame_rate = int(self.bg_cap.get(cv2.CAP_PROP_FPS))
			self.outmp4 = cv2.VideoWriter(self.out_path,cv2.VideoWriter_fourcc('M','J','P','G'), self.frame_rate, (self.w, self.h))

		else:
			self.output_type = 'image'
			self.finished = True


	def fg(self):
		# Update foreground frame (only for mp4)
		if (self.fg_ext in video_extensions) and (self.finished == False): 
			ret, frame = self.fg_cap.read()
			if ret == True:
				self.fg_frame = frame
			else:
				if self.reference == 'foreground':
					self.finished = True
					self.fg_cap.release()
					if self.bg_ext in video_extensions:
						self.bg_cap.release()
		return self.fg_frame

	def bg(self):
		# Update background frame (only for mp4)
		if (self.bg_ext in video_extensions) and (self.finished == False): 
			ret, frame = self.bg_cap.read()
			if ret == True:
				self.bg_frame = frame
			else:
				if self.reference == 'background':
					self.finished = True
					self.bg_cap.release()
		return self.bg_frame

	def write(self, frame):
		if (self.output_type=='video'):	
			if (self.finished == False):
				self.outmp4.write(frame)
			else:
				self.outmp4.release()
		else:
			cv2.imwrite(self.out_path, frame)