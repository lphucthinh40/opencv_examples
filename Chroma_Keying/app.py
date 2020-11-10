import cv2
import argparse
import numpy as np

from media import MediaHandler
from chromakey import ChromaKey

# NOTE: 
# - For default input, USE: python app.py
# - Drag & release to select sample region at the start of the program.
# - Both background & foreground need to have the same resolution
# - Each background & foreground can accept either image or video, TRY:
# 		python app.py -o output/out_1.mp4 -f data/fg_1_720.mp4 -b data/bg_1_720.mp4 -tla 80 -tlb 100
# 		python app.py -o output/out_2.mp4 -f data/fg_2_720.mp4 -b data/bg_2_720.jpg -tla 40 -tlb 50
# 		python app.py -o output/out_2.jpg -f data/fg_2_1080.jpg -b data/bg_2_1080.jpg -tla 40 -tlb 50
# - Following the reference material (http://gc-films.com/chromakey.html) with some modifications

DEFAULT_FG = "data/fg_1_720.mp4"
DEFAULT_BG = "data/bg_1_720.mp4"
DEFAULT_OUT = "output/out_1.mp4"
WINDOW_NAME = "MainWindow"

pt0 = None
pt1 = None
key_sampled = False
chroma = None

# _______ CALLBACK HANDLERS ______

def scaleTol(*args):
    global chroma
    chroma.tolA = args[0]
    if key_sampled:
    	chroma.process()

def scaleSoft(*args):
	global chroma
	chroma.tolB = chroma.tolA + args[0]
	if key_sampled:
		chroma.process()

def scaleDesat(*args):
    global chroma
    chroma.deSat = float(args[0]/200) # limit maximum to 0.5
    if key_sampled:
    	chroma.process()

def sample(action, x, y, flags, userdata):
	global pt0, pt1, chroma, key_sampled
	if (key_sampled == False):
		if action==cv2.EVENT_LBUTTONDOWN:
			pt0=(x,y)
		if action==cv2.EVENT_LBUTTONUP:
			pt1=(x,y)
			chroma.output = cv2.rectangle(chroma.output, pt0, pt1, (255,0,0), 2)
			cv2.imshow("MainWindow", chroma.output)
			chroma.sampleKey([pt0[0], pt0[1], pt1[0], pt1[1]])
			key_sampled = True
			cv2.waitKey(100)
			chroma.output = np.copy(chroma.imgBGR)
			chroma.process()


# _______ MAIN ______
def main(out_path, fg_path, bg_path, tolA, tolB, deSat):
	global key_sampled, chroma
	media = MediaHandler(fg_path, bg_path, out_path)
	chroma = ChromaKey(tolA, tolB, deSat)
	chroma.loadImage(media.fg())
	chroma.loadBackground(media.bg())

	# put text on the first output
	cv2.putText(chroma.output,"Drag and release to collect sample. Press ESC to exit.",
	(10,20), cv2.FONT_HERSHEY_SIMPLEX,
	0.75,(255,255,255), 2 );

	cv2.namedWindow(WINDOW_NAME)
	cv2.setMouseCallback(WINDOW_NAME, sample)
	cv2.createTrackbar("Lower Limit (TolA) :", WINDOW_NAME, tolA, 100, scaleTol)
	cv2.createTrackbar("Blending Region (TolB-TolA):", WINDOW_NAME, tolB-tolA, 100, scaleSoft)
	cv2.createTrackbar("Desaturation:", WINDOW_NAME, deSat, 100, scaleDesat)

	k=0
	# wait for escape key
	while k!=27:
		cv2.imshow("MainWindow", chroma.output)
		if (key_sampled) and (media.finished == False):
			chroma.loadImage(media.fg())
			chroma.loadBackground(media.bg())
			chroma.process()
			media.write(chroma.output)

		k = cv2.waitKey(1) & 0xFF
	# add this to save image
	if (media.output_type == 'image'):
		media.write(chroma.output)

if __name__ == '__main__':
	ap = argparse.ArgumentParser(description='Chroma Keying App')
	ap.add_argument('-o', metavar='OutputName', type=str, help='name of the output file', default=DEFAULT_OUT)
	ap.add_argument('-f', metavar='Foreground', type=str, help='path to foreground media file (mp4, jpg, or png)', default=DEFAULT_FG)
	ap.add_argument('-b', metavar='Background', type=str, help='path to background media file (mp4, jpg, or png)', default=DEFAULT_BG)
	ap.add_argument('-tla', metavar='ToleranceA', type=int, help='Tolerance A Parameter', default=80)
	ap.add_argument('-tlb', metavar='ToleranceB', type=int, help='Tolerance B Parameter', default=100)
	ap.add_argument('-d', metavar='Desaturation', type=int, help='Desaturation Parameter', default=10)

	args = ap.parse_args()
	
	main(args.o, args.f, args.b, args.tla, args.tlb, args.d)
