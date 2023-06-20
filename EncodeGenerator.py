import os
import cv2
import face_recognition
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e4d4b-default-rtdb.firebaseio.com/",
    "storageBucket" : "faceattendance-e4d4b.appspot.com"
})




#Importing student images

folderPath = 'images'
PathList = os.listdir(folderPath)
imgList = []
StudentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    StudentIds.append(os.path.splitext(path)[0])

    #for database access
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        #converting bgr image color(used by opencv) to RGB image (used by face-recogntiion)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0] 
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDS = [encodeListKnown, StudentIds]

file = open("EncodeFile.p" , "wb")
pickle.dump(encodeListKnownWithIDS,file)
file.close()
print("File Saved")