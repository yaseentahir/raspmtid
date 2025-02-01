import logging
import threading
import cv2
import cv2 as cv
import numpy as np

USE_FAKE_PI_CAMERA = True # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_PI_CAMERA:
    from .camera import Camera  # For running app
else:
    from .pi_camera import Camera  # For running Raspberry Pi

log = logging.getLogger(
    __name__)  # Creates a logger instance, we use it to log things out


class OpenCVController(object):

    def __init__(self):
        self.current_shape = [False, False, False]
        self.camera = Camera()
        print('OpenCV controller initiated')

    def process_frame(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            frame = self.camera.get_frame()  # read the camera frame
            ###Process frame here
            inputImage = frame.copy()
            if not USE_FAKE_PI_CAMERA:
                # Define the crop size and center point
                height, width = 370, 650
                center_x, center_y = inputImage.shape[1] / 2, inputImage.shape[0] / 2
                # Perform the crop
                inputImage = cv2.getRectSubPix(inputImage, (width, height), (center_x, center_y))
            finalImageMark,Result=redMarkdetection(inputImage)
            boxesDigit,boxes=digitdetection(finalImageMark)
            frame=drawBox(finalImageMark,boxes,boxesDigit)
            self.current_shape=Result
           
            return frame
    def get_current_shape(self):
        return self.current_shape


def createBox(boxinfo):
    xmin=10000
    xmax=0
    y=1000
    for i in boxinfo:
        xvalue=i[0]
        yvalue=i[1]
        if(xmax<xvalue):
            xmax=xvalue
        if(xmin>xvalue):
            xmin=xvalue
        if(y>yvalue):
            y=yvalue
    boxresult=[]
    xsub1=40
    xsub2=15
    if(y>300):
        y=625-y
    diff=(xmax-xsub2)-(xmin-xsub1)
    nextvalue=(xmax-xsub2)+diff
    boxresult.append([xmin-xsub1,y,330,460])
    boxresult.append([xmax-xsub2,y,290,460])
    boxresult.append([nextvalue-25,y,315,460])
    
    
    return boxresult
def drawBox(image,boxes,boxesDigit):
    i=0
    testImage=image
    for box in boxes:
        y=box[1]
        top_left     = (box[0], box[1])
        bottom_right = (box[0] + box[2], box[1] + box[3])
        x= bottom_right[0]-20
        y=bottom_right[1]-20
        cv2.rectangle(testImage, top_left, bottom_right, (0,255,0), 10)
        pos=[x,y]
        text=str(boxesDigit[i])
        font=cv2.FONT_HERSHEY_DUPLEX
        font_scale=2.0
        font_thickness=6
        text_color_bg=(0, 255, 0)
        text_color=(255,255,255)
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv2.rectangle(testImage, pos, (x + text_w, y + text_h), text_color_bg, -1)
        cv2.putText(testImage, text, (x, (y + text_h )), font, font_scale, text_color, font_thickness)
        i=i+1
    return testImage
def ImageShow(inputImage,imageName):
    cv2.imshow(imageName, inputImage)
    cv2.waitKey(0)
def digitdetection(image):
    inputImage = image
    # Convert RGB to grayscale:
    grayscaleImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    binaryThresh =100
    _, binaryImage = cv2.threshold(grayscaleImage, binaryThresh, 255, cv2.THRESH_BINARY)
    imageInver=~binaryImage
    contours, _ = cv2.findContours(imageInver, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    point=0
    newPoint=[]
    boxesDigit=[8,3,1]
    # list for storing names of shapes
    for contour in contours:
        # here we are ignoring first counter because 
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue
        i=i+1
        # cv2.approxPloyDP() function to approximate the shape
        #cv2.drawContours(inputImage, [contour], 0, (i, i, 255), 5)
        approx = cv2.approxPolyDP(
            contour, 0.07 * cv2.arcLength(contour, True), True)
        x1, y1, w, h = cv2.boundingRect(contour)
        
        if(len(approx)==2 and h>400 and w>25 and w<50):
            if(point==0):
                #newPoint.append([x1,y1,w,h])
                #cv2.drawContours(inputImage, [contour], 0, (0, 0, 255), 5)
                point=point+1
                #print("width : ",w,"height: ",h)
        elif(len(approx)==2 and w>200 and h>23 and h<30 and w<260):
            #cv2.drawContours(inputImage, [contour], 0, (0, 0, 255), 5)
            newPoint.append([x1,y1,w,h])
            
        else:
            if(w>200 and w<280 and h<35):
                
                newPoint.append([x1,y1,w,h])
       
            #newPoint.append([x1,y1,w,h])
       
            
    
    box=createBox(newPoint)
    return boxesDigit,box
def redMarkPositionDetection(point,mask,original):
    x=point[0]
    y=point[1]
    w=point[2]
    h=point[3]
    crop_img = mask[y:y+h, x:x+w]
    crop_img1 = original[y:y+h, x:x+w]
    n_white_pix = np.sum( crop_img == 255)
    if(n_white_pix>1000):
        return True
    return False
def redMarkdetection(image):
    inputImage = image
    ROI=image
    grayscaleImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    # Convert the BGR image to HSV:
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    # Create the HSV range for the blue ink:
    # [128, 255, 255], [90, 50, 70]
    lowerValues = np.array([170,50,50])
    upperValues = np.array([180,255,255])
    point1=[215,75,337,626]
    point2=[555,85,337,626]
    point3=[897,63,337,626]
    # Get binary mask of the blue ink:
    redpenMask = cv2.inRange(hsvImage, lowerValues, upperValues)
    # Use a little bit of morphology to clean the mask:
    # Set kernel (structuring element) size:
    kernelSize = 3
    # Set morph operation iterations:
    opIterations = 1
    # Get the structuring element:
    morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
    # Perform closing:
    redpenMask = cv2.morphologyEx(redpenMask, cv2.MORPH_CLOSE, morphKernel, None, None, opIterations, cv2.BORDER_REFLECT101)
    # Add the white mask to the grayscale image:
    colorMask = cv2.add(grayscaleImage, redpenMask)
    _, binaryImage = cv2.threshold(colorMask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh, im_bw = cv2.threshold(binaryImage, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    imgfinal = cv2.dilate(im_bw, kernel=kernel, iterations=1)
    result1=redMarkPositionDetection(point1,redpenMask,inputImage)
    result2=redMarkPositionDetection(point2,redpenMask,inputImage)
    result3=redMarkPositionDetection(point3,redpenMask,inputImage)
    result=[result1,result2,result3]
    
    contours, hierarchy = cv2.findContours(redpenMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    
    for ctr in contours:
        x, y, w, h = cv2.boundingRect(ctr)
        if w > 50 and h>200:
            boxes.append([x, y, w, h])
            
            
    for box in boxes:
        top_left     = (box[0], box[1])
        bottom_right = (box[0] + box[2], box[1] + box[3])
        cv2.rectangle(ROI, top_left, bottom_right, (0,0,255), 10)
        x= bottom_right[0]-130
        y=bottom_right[1]+30
        pos=[x,y]
        text='Red Mark'
        font=cv2.FONT_HERSHEY_DUPLEX
        font_scale=1.5
        font_thickness=2
        text_color_bg=(0, 0, 255)
        text_color=(255,255,255)
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv2.rectangle(ROI, pos, (x + text_w, y + text_h), text_color_bg, -1)
        cv2.putText(ROI, text, (x, (y + text_h )), font, font_scale, text_color, font_thickness)
    
    return ROI,result
