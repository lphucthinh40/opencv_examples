import numpy as np
import cv2

def getColorBackground(color, shape):
    bg = np.ones(shape, dtype=np.uint8)
    bg = bg * np.array(list(color), dtype=np.uint8)
    return bg

class ChromaKey:
    def __init__(self, toleranceA=80, toleranceB=100, deSat = 10):
        self.tolA = toleranceA
        self.tolB = toleranceB
        self.deSat = deSat/100
        self.keyBGR = None
        self.imgBGR = None
        self.imgYCC = None
        self.output = None
        
    def updateTolerance(tolA, tolB):
        self.tolA = tolA
        self.tolB = tolB
        
    def loadImage(self, image):
        self.imgBGR = image
        self.imgYCC = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        self.output = np.copy(image)
        
    def loadBackground(self, image):
        self.bgBGR = image
                
    def sampleKey(self, roi):
        if not (self.imgBGR is None):
            self.keyBGR = np.mean(self.imgBGR[roi[0]:roi[2], roi[1]:roi[3]], axis=(0,1))
            self.keyYCC = np.mean(self.imgYCC[roi[0]:roi[2], roi[1]:roi[3]], axis=(0,1))
    
    def process(self):
        # Generate Alpha mask
        self.relvec =(self.imgYCC[:,:,1]-self.keyYCC[1])**2+(self.imgYCC[:,:,2]-self.keyYCC[2])**2
        self.relvec = np.sqrt(self.relvec)
        self.alpha = np.ones_like(self.relvec, dtype=np.float)
        if (self.tolB > self.tolA):
            self.alpha = (self.relvec - self.tolA) / (self.tolB - self.tolA)
            self.alpha[self.relvec <  self.tolA] = 0
            self.alpha[self.relvec >= self.tolB] = 1
        else:
            self.alpha[self.relvec <  self.tolA] = 0
            self.alpha[self.relvec >= self.tolA] = 1
        self.alpha = np.stack((self.alpha,)*3, axis=-1)

        # Desaturate key color in foreground
        fg = self.imgBGR * self.alpha
        fg = fg.astype(np.float) - self.keyBGR.astype(float) * self.deSat
        fg = fg.clip(min=0).astype(np.uint8)
        
        # Combine foreground & background
        bg = self.bgBGR * (1-self.alpha)
        self.output = (fg + bg).astype(np.uint8)