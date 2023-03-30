from datetime import datetime
import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e4d4b-default-rtdb.firebaseio.com/",
    "storageBucket" : "faceattendance-e4d4b.appspot.com"
})

bucket  = storage.bucket()

#for accessing webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4,480)

imgBackground = cv2.imread('resources/background.png')

#importing mode images in list 
foldeModePath = 'resources/Modes'
modePathList = os.listdir(foldeModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(foldeModePath,path)))


#Load the encoding File
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIDS = pickle.load(file)
file.close()
encodeListKnown, StudentIds = encodeListKnownWithIDS
#print(StudentIds)
#print(encodeListKnown)



modeType = 0
counter = 0
id=0
imgStudent = []

#for accessing webcam
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)



    #to overlay webcam on the graphics image
    imgBackground[162:162+480 , 55:55+640] = img
    imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]
    
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDist = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print("matches",matches)
            #print("faceDistance", faceDist)


            matchIndex = np.argmin(faceDist)
            #print("Match Index", matchIndex)

            if matches[matchIndex]:
                #print("Roll no: ",StudentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = StudentIds[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter !=0 :
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                #get the image from the storage
                blob = bucket.get_blob(f'images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_tim'],
                                                "%Y-%m-%d %H:%M:%S")    
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_tim').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]

            
            if modeType != 3:

                if 10<counter<20:
                    modeType = 2
                imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    (w,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445), cv2.FONT_HERSHEY_COMPLEX,1,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['Course']),(1006,550), cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(id),(1006,493), cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['standing']),(910,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['Passing Year']),(1025,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['last_attendance_tim']),(1125,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)


                    imgBackground[175:175+216,909:909+216] = imgStudent
            
            
                counter+=1

                if counter>=20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]
        
    else:
        modeType = 0
        counter = 0


            
    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)