import cv2
import numpy as np
import os

orb = cv2.ORB_create(nfeatures = 1000)
path = 'ImagesQuery'
images = []
classNames = []
myList = os.listdir(path)
print('Total Classes Detected: ', len(myList))

for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}', 0)
    images.append(imgCur)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img,None)
        desList.append(des)
    return desList

def findID(img, desList, threshold = 10):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    final_val = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des,des2,k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
        print(matchList)
    except:
        pass
    
    if len(matchList) != 0:
        if max(matchList) > threshold:
            final_val = matchList.index(max(matchList))
        return final_val

desList = findDes(images)
print(len(desList))

cap = cv2.VideoCapture(0)

while True:

    success, img2 = cap.read()
    imgOrig = img2.copy()
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    
    id = findID(img2,desList)
    if id != -1:
        if id == None:
            cv2.putText(imgOrig, 'No Object',(50,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(imgOrig, classNames[id],(50,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('image', imgOrig)
    if cv2.waitKey(1)==27:
        break