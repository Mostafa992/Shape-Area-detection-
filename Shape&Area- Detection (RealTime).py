import cv2
import numpy as np



cap=cv2.VideoCapture(0)
cap.set(3,620)
cap.set(4,480)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,280)
cv2.createTrackbar("Thresh 1","Parameters",100,255,empty)
cv2.createTrackbar("Thresh 2","Parameters",255,255,empty)
cv2.createTrackbar("Min Area","Parameters",1000,10000,empty)

def getContours(img, imgContour):
    contours, hiearchy = cv2.findContours(frameEroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt, True)
        minArea=cv2.getTrackbarPos("Min Area","Parameters")
        if area>minArea:
            cv2.drawContours(imgContour, cnt, -1, (6, 6, 146), 5)
            perimeter=cv2.arcLength(cnt,True)
            accuarcy=perimeter*0.02
            approx=cv2.approxPolyDP(cnt,accuarcy,True)
            x,y,w,h=cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(155,0,0),5)

            cv2.putText(imgContour,"Points: "+ str(len(approx)),(x+w,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)
            cv2.putText(imgContour,"Area: "+ str(int(area)),(x+w,y+20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)

while True:
    _,frame=cap.read()
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frameBlur=cv2.GaussianBlur(frameGray,(7,7),1)
    threshold1=cv2.getTrackbarPos("Thresh 1","Parameters")
    threshold2=cv2.getTrackbarPos("Thresh 1","Parameters")
    frameCanny=cv2.Canny(frameBlur,threshold1,threshold2)
    kernel=np.ones((5,5))
    frameDilation=cv2.dilate(frameCanny,kernel=kernel,iterations=2)
    frameEroded=cv2.erode(frameDilation,(5,5),iterations=1)


    imgContour=frame.copy()


    getContours(frame,imgContour)
    cv2.imshow("FrameOrignal",frame)
    cv2.imshow("Contours",imgContour)
    cv2.imshow("Canny",frameCanny)
    cv2.imshow("Dilation",frameDilation)




    if cv2.waitKey(1)&0xff==27:
        break
cap.release()
cv2.destroyAllWindows()