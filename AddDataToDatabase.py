
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e4d4b-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "3":{
    "name" : "Adil Shaikh",
    "Course" : "B-Tech",
    "Passing Year" : 2024,
    "total_attendance" : 5,
    "standing" : "VG",
    "last_attendance_time" : "2023-6-"
    }
}

for key,value in data.items():
    ref.child(key).set(value)