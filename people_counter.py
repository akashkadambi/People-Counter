#PEOPLE COUNTER TO AVOID CROWD GATHERINGS

import cv2
import imutils
import numpy as np
from twilio.rest import Client
import keys
import winsound

def send_alert(count):
    for i in range(0,3):
        winsound.PlaySound("./beep.wav", winsound.SND_ALIAS)
        client=Client(keys.account_sid,keys.auth_token)
        client.messages.create(body="OVER CROWDING! CLEAR THE AREA!",from_=keys.twilio_number,to=keys.target_number)

def spot_humans(pic,limit):
    areas,probs=Hog.detectMultiScale(pic,scale=1.02,winStride=(4,4),padding=(8,8)) #processing every window
    
    finalareas=[]
    for i in range(0,len(probs)):
        if(probs[i]>0.1):
            finalareas.append(list(areas[i]))
    people=np.array(finalareas)
    
    count=0
    for x,y,w,h in people:
        count+=1
        cv2.rectangle(pic,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(pic,f'person {count}',(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,69,255),2)
    
    if(count<=limit):
        cv2.putText(pic,f'Total : {count}',(30,30),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,0,0),2)
        alertflag=0
    else:
        cv2.putText(pic,f'Total : {count}',(30,30),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,255),2)
        alertflag=1
    
    return (pic,alertflag,count)

def Piccount(limit):
    path=input("Enter the path-name of the picture:\n")
    pic=cv2.imread(path)
    pic=imutils.resize(pic,width=min(800,np.shape(pic)[1])) #Small size for better detection
    spotted_pic,alert,count=spot_humans(pic,limit) 
    cv2.imshow("Spotted Pic",spotted_pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if(alert):
        send_alert(count)
    return

def Vidcount(limit):
    path=input("Enter the path-name of the video:\n")
    vid=cv2.VideoCapture(path)
    
    flag,pic=vid.read()
    if(flag==False):
        print('File Not Read! Enter Valid Path')
        return
    
    alertflag=1
    
    while vid.isOpened():
        flag,pic=vid.read()
        if(flag):
            pic=imutils.resize(pic,width=min(800,pic.shape[1]))
            spotted_pic,alert,count=spot_humans(pic,limit)
            cv2.imshow("Spotted Video",spotted_pic)
            if(alert and alertflag):
                send_alert(count)
                alertflag=0
            
            key=cv2.waitKey(30)
            if(key==ord('q')):
                break
            elif(key==ord('r')):
                alertflag=1
        else:
            break
    vid.release()
    cv2.destroyAllWindows()

def Camcount(limit):
    vid=cv2.VideoCapture(0)
    alertflag=1
    
    while vid.isOpened():
        flag,pic=vid.read()
        if(flag):
            pic=imutils.resize(pic,width=min(800,pic.shape[1]))
            spotted_pic,alert,count=spot_humans(pic,limit)
            cv2.imshow("Spotted Camera",spotted_pic)
            if(alert and alertflag):
                send_alert(count)
                alertflag=0
            
            key=cv2.waitKey(30)
            if(key==ord('q')):
                break
            elif(key==ord('r')):
                alertflag=1
        else:
            break
    vid.release()
    cv2.destroyAllWindows()

opt=int(input("From What You Want To Count?\n1 : Photo\n2 : Video\n3 : Camera\n"))
limit=int(input("Enter the crowd gathering limit\n"))

Hog=cv2.HOGDescriptor()  #Gradient Filter
Hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) #SVM to classify into human class
if(limit<=0):
    print("Invalid Number! Enter +ve number only")
if(opt==1):
    Piccount(limit)
elif(opt==2):
    Vidcount(limit)
elif(opt==3):
    Camcount(limit)
else:
    print("Invalid Number! Enter only 1 or 2 or 3")