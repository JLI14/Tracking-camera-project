import mss
import numpy as np
import cv2
from PIL import ImageGrab
import webbrowser
import time
import socket
import keyboard

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap=cv2.VideoCapture(0)

ipaddress=raw_input('Please type in the camera ipaddress:')
strPort=input('Please enter the available port')
Port=int(strPort)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ipaddress, Port))                     #                                                    I

webbrowser.open("http://"+str(ipaddress)+":8000")

defaultxangle=90
defaultyangle=90
change=True
locw=-1
swaploc=False


def take(x,y,w,h):#The factory camera for the Raspberry Pi comes with a tiny lens that has a Field of View of about 67 degrees diagonal(53 degrees Horizontal and 41 degrees Vertical)
    
    global defaultxangle
    global defaultyangle
    global change
    
    print("x:"+str(x)+" y:"+str(y)+" side:"+str(w))
    
    if(x+(w/2)<440 or x+(w/2)>500):
        angle=((float(x)+(float(w/2)-480))/640)*53
        print("added angle:"+str(angle))
        defaultxangle=defaultxangle - angle
       
    if(y+(h/2)<360 or y+(h/2)>400):
        angle=((float(y)+(float(h/2))-360)/480)*41
        print("added angle:"+str(angle))
        defaultyangle= defaultyangle - angle
        
    if(defaultxangle>180):
        defaultxangle=180
        
    if(defaultxangle<0):
        defaultxangle=0
        
    if(defaultyangle>180):
        defaultyangle=180
        
    if(defaultyangle<0):
        defaultyangle=0
        
    defaultxangle=int(defaultxangle)
    defaultyangle=int(defaultyangle)
    
    if(x+(w/2)<440 or x+(w/2)>500):
        output='x'+str(defaultxangle)
        print(output)
        s.send(output)
        change=False
        if s.recv(1024)=="confirmed":
            change=True
            
    if(y+(h/2)<360 or y+(h/2)>400):
        output='y'+str(defaultyangle)
        print(output)
        s.send(output)
        change=False
        if s.recv(1024)=="confirmed":
            change=True

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {'top': 150, 'left': 450, 'width': 640, 'height': 480}#---------------------------------+--------------------------------------------}

    while 'Screen capturing':
        
        try:  #used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('r'):  # if key 'r' is pressed
                for x in range(0,5):
                    s.send('Calibrating distance in: '+str(5-x)+ '(please stand 1 meter from the camera)')
                    time.sleep(1)
                    
                s.send('Calibrating distance...')
                swaploc=True
        except:
            print('no valid key is pressed')


        
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array                                    I
        img = np.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow('OpenCV/Numpy normal', img)

        # Display the picture in grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 0)#------------------------------------+
                roi_gray = gray[y:y+h, x:x+w]           #}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
                roi_color =img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                
                if change==True:
                    print("x:"+str(x)+" y:"+str(y)+" side:"+str(w))
                    take(x,y,w,h)

                if(swaploc==True):
                    locw=float(w*1)/0.5
                    
                    s.send('Distance calibrated!')
                    
                    swaploc=False

                if(locw!=-1):
                    distance=locw*0.5/w
                    
                    s.send('target is '+str(distance)+' meters from the camera')
                    
                    

                for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color, (ex,ey),(ex+ew,ey+eh), (0, 255,0),2)

        #print('fps: {0}'.format(1 / (time.time()-last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


cap.release()
cv2.destroyAllWindows()
    








